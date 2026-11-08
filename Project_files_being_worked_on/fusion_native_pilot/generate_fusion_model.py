"""Create native Fusion sketch-and-extrude components from a JSON model spec.

Run this script inside Autodesk Fusion from Tools > Scripts and Add-Ins.
The output is an F3D archive containing Fusion-native component sketches,
dimensions, user parameters, and extrusion features.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import traceback
from datetime import datetime, timezone

import adsk.core
import adsk.fusion


PILOT_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGED_SCRIPT_DIR = os.path.join(PILOT_DIR, "generate_fusion_model")
SCRIPT_DIR = (
    PACKAGED_SCRIPT_DIR
    if os.path.isfile(
        os.path.join(PACKAGED_SCRIPT_DIR, "generate_fusion_model.manifest")
    )
    else PILOT_DIR
)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from fusion_model_spec import (
    expected_component_extents_mm,
    safe_file_stem,
    validate_model_spec,
)
from fusion_spec_batch import normalize_selected_spec_paths


SCRIPT_VERSION = "1.2.0"


def _unique_base(output_dir: str, stem: str) -> str:
    candidate = os.path.join(output_dir, stem)
    suffix = 2
    while any(
        os.path.exists(candidate + extension)
        for extension in (".f3d", "-report.json")
    ):
        candidate = os.path.join(output_dir, f"{stem}-{suffix:02d}")
        suffix += 1
    return candidate


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _add_length_parameter(design, name: str, value_mm: float, comment: str) -> str:
    parameter = design.userParameters.add(
        name,
        adsk.core.ValueInput.createByString(f"{value_mm:.12g} mm"),
        "mm",
        comment,
    )
    if not parameter:
        raise RuntimeError(f"Fusion could not create parameter {name}.")
    return name


def _set_parameter_expression(dimension, expression: str) -> None:
    if not dimension or not dimension.parameter:
        raise RuntimeError("Fusion could not create a driving sketch dimension.")
    dimension.parameter.expression = expression


def _create_box(design, component, component_spec, parameter_prefix: str):
    dimensions = component_spec["dimensions_mm"]
    length_mm = dimensions["length"]
    width_mm = dimensions["width"]
    height_mm = dimensions["height"]

    length_param = _add_length_parameter(
        design, f"{parameter_prefix}_Length", length_mm, "Overall component length"
    )
    width_param = _add_length_parameter(
        design, f"{parameter_prefix}_Width", width_mm, "Overall component width"
    )
    height_param = _add_length_parameter(
        design, f"{parameter_prefix}_Height", height_mm, "Extrusion height"
    )

    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = f"{component_spec['name']} Profile"
    lines = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(length_mm / 10.0, width_mm / 10.0, 0),
    )
    if not lines or lines.count != 4:
        raise RuntimeError(f"Fusion failed to sketch box {component_spec['name']}.")

    constraints = sketch.geometricConstraints
    constraints.addHorizontal(lines.item(0))
    constraints.addVertical(lines.item(1))
    constraints.addHorizontal(lines.item(2))
    constraints.addVertical(lines.item(3))
    constraints.addCoincident(lines.item(0).startSketchPoint, sketch.originPoint)

    length_cm = length_mm / 10.0
    width_cm = width_mm / 10.0
    length_dimension = sketch.sketchDimensions.addDistanceDimension(
        lines.item(0).startSketchPoint,
        lines.item(0).endSketchPoint,
        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(length_cm / 2.0, -max(width_cm * 0.2, 0.5), 0),
    )
    width_dimension = sketch.sketchDimensions.addDistanceDimension(
        lines.item(1).startSketchPoint,
        lines.item(1).endSketchPoint,
        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
        adsk.core.Point3D.create(length_cm + max(length_cm * 0.2, 0.5), width_cm / 2.0, 0),
    )
    _set_parameter_expression(length_dimension, length_param)
    _set_parameter_expression(width_dimension, width_param)

    profile = sketch.profiles.item(0)
    extrude = component.features.extrudeFeatures.addSimple(
        profile,
        adsk.core.ValueInput.createByString(height_param),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    if not extrude or extrude.bodies.count != 1:
        raise RuntimeError(f"Fusion failed to extrude box {component_spec['name']}.")
    extrude.name = f"{component_spec['name']} Extrusion"
    body = extrude.bodies.item(0)
    body.name = component_spec["name"]
    return body, {
        "length": length_param,
        "width": width_param,
        "height": height_param,
    }


def _create_cylinder(design, component, component_spec, parameter_prefix: str):
    dimensions = component_spec["dimensions_mm"]
    diameter_mm = dimensions["diameter"]
    height_mm = dimensions["height"]

    diameter_param = _add_length_parameter(
        design,
        f"{parameter_prefix}_Diameter",
        diameter_mm,
        "Overall cylinder diameter",
    )
    height_param = _add_length_parameter(
        design, f"{parameter_prefix}_Height", height_mm, "Extrusion height"
    )

    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = f"{component_spec['name']} Profile"
    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(0, 0, 0), diameter_mm / 20.0
    )
    if not circle:
        raise RuntimeError(
            f"Fusion failed to sketch cylinder {component_spec['name']}."
        )
    sketch.geometricConstraints.addCoincident(
        circle.centerSketchPoint, sketch.originPoint
    )
    radial_dimension = sketch.sketchDimensions.addRadialDimension(
        circle,
        adsk.core.Point3D.create(
            diameter_mm / 20.0 * 1.7, diameter_mm / 20.0 * 1.2, 0
        ),
    )
    _set_parameter_expression(radial_dimension, f"{diameter_param} / 2")

    profile = sketch.profiles.item(0)
    extrude = component.features.extrudeFeatures.addSimple(
        profile,
        adsk.core.ValueInput.createByString(height_param),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    if not extrude or extrude.bodies.count != 1:
        raise RuntimeError(
            f"Fusion failed to extrude cylinder {component_spec['name']}."
        )
    extrude.name = f"{component_spec['name']} Extrusion"
    body = extrude.bodies.item(0)
    body.name = component_spec["name"]
    return body, {"diameter": diameter_param, "height": height_param}


def _profile_with_loop_count(sketch, loop_count: int, component_name: str):
    matches = []
    for index in range(sketch.profiles.count):
        profile = sketch.profiles.item(index)
        if profile.profileLoops.count == loop_count:
            matches.append(profile)
    if len(matches) != 1:
        raise RuntimeError(
            f"Fusion could not identify the {loop_count}-loop profile for "
            f"{component_name}; found {len(matches)} candidates."
        )
    return matches[0]


def _create_annular_cylinder(design, component, component_spec, parameter_prefix: str):
    dimensions = component_spec["dimensions_mm"]
    outer_diameter_mm = dimensions["outer_diameter"]
    inner_diameter_mm = dimensions["inner_diameter"]
    height_mm = dimensions["height"]

    outer_diameter_param = _add_length_parameter(
        design,
        f"{parameter_prefix}_OuterDiameter",
        outer_diameter_mm,
        "Preliminary outer diameter",
    )
    inner_diameter_param = _add_length_parameter(
        design,
        f"{parameter_prefix}_InnerDiameter",
        inner_diameter_mm,
        "Preliminary bore diameter",
    )
    height_param = _add_length_parameter(
        design, f"{parameter_prefix}_Height", height_mm, "Extrusion height"
    )

    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = f"{component_spec['name']} Profile"
    origin = adsk.core.Point3D.create(0, 0, 0)
    outer_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        origin, outer_diameter_mm / 20.0
    )
    inner_circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        origin, inner_diameter_mm / 20.0
    )
    if not outer_circle or not inner_circle:
        raise RuntimeError(
            f"Fusion failed to sketch annular cylinder {component_spec['name']}."
        )

    constraints = sketch.geometricConstraints
    constraints.addCoincident(outer_circle.centerSketchPoint, sketch.originPoint)
    constraints.addCoincident(inner_circle.centerSketchPoint, sketch.originPoint)
    outer_dimension = sketch.sketchDimensions.addRadialDimension(
        outer_circle,
        adsk.core.Point3D.create(
            outer_diameter_mm / 20.0 * 1.4,
            outer_diameter_mm / 20.0 * 1.2,
            0,
        ),
    )
    inner_dimension = sketch.sketchDimensions.addRadialDimension(
        inner_circle,
        adsk.core.Point3D.create(
            -inner_diameter_mm / 20.0 * 1.5,
            -inner_diameter_mm / 20.0 * 1.1,
            0,
        ),
    )
    _set_parameter_expression(outer_dimension, f"{outer_diameter_param} / 2")
    _set_parameter_expression(inner_dimension, f"{inner_diameter_param} / 2")

    profile = _profile_with_loop_count(sketch, 2, component_spec["name"])
    extrude = component.features.extrudeFeatures.addSimple(
        profile,
        adsk.core.ValueInput.createByString(height_param),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    if not extrude or extrude.bodies.count != 1:
        raise RuntimeError(
            f"Fusion failed to extrude annular cylinder {component_spec['name']}."
        )
    extrude.name = f"{component_spec['name']} Extrusion"
    body = extrude.bodies.item(0)
    body.name = component_spec["name"]
    return body, {
        "outer_diameter": outer_diameter_param,
        "inner_diameter": inner_diameter_param,
        "height": height_param,
    }


def _create_plate_with_bore(design, component, component_spec, parameter_prefix: str):
    dimensions = component_spec["dimensions_mm"]
    length_mm = dimensions["length"]
    width_mm = dimensions["width"]
    height_mm = dimensions["height"]
    bore_diameter_mm = dimensions["bore_diameter"]

    length_param = _add_length_parameter(
        design, f"{parameter_prefix}_Length", length_mm, "Plate length"
    )
    width_param = _add_length_parameter(
        design, f"{parameter_prefix}_Width", width_mm, "Plate width"
    )
    height_param = _add_length_parameter(
        design, f"{parameter_prefix}_Height", height_mm, "Plate thickness"
    )
    bore_diameter_param = _add_length_parameter(
        design,
        f"{parameter_prefix}_BoreDiameter",
        bore_diameter_mm,
        "Preliminary centered bore diameter",
    )

    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = f"{component_spec['name']} Profile"
    lines = sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(0, 0, 0),
        adsk.core.Point3D.create(length_mm / 10.0, width_mm / 10.0, 0),
    )
    if not lines or lines.count != 4:
        raise RuntimeError(
            f"Fusion failed to sketch plate {component_spec['name']}."
        )

    constraints = sketch.geometricConstraints
    constraints.addHorizontal(lines.item(0))
    constraints.addVertical(lines.item(1))
    constraints.addHorizontal(lines.item(2))
    constraints.addVertical(lines.item(3))
    constraints.addCoincident(lines.item(0).startSketchPoint, sketch.originPoint)

    length_cm = length_mm / 10.0
    width_cm = width_mm / 10.0
    length_dimension = sketch.sketchDimensions.addDistanceDimension(
        lines.item(0).startSketchPoint,
        lines.item(0).endSketchPoint,
        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(length_cm / 2.0, -max(width_cm * 0.2, 0.5), 0),
    )
    width_dimension = sketch.sketchDimensions.addDistanceDimension(
        lines.item(1).startSketchPoint,
        lines.item(1).endSketchPoint,
        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
        adsk.core.Point3D.create(
            length_cm + max(length_cm * 0.2, 0.5), width_cm / 2.0, 0
        ),
    )
    _set_parameter_expression(length_dimension, length_param)
    _set_parameter_expression(width_dimension, width_param)

    circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(length_cm / 2.0, width_cm / 2.0, 0),
        bore_diameter_mm / 20.0,
    )
    if not circle:
        raise RuntimeError(f"Fusion failed to sketch bore in {component_spec['name']}.")
    bore_dimension = sketch.sketchDimensions.addRadialDimension(
        circle,
        adsk.core.Point3D.create(
            length_cm / 2.0 + bore_diameter_mm / 20.0 * 1.7,
            width_cm / 2.0 + bore_diameter_mm / 20.0 * 1.2,
            0,
        ),
    )
    center_x_dimension = sketch.sketchDimensions.addDistanceDimension(
        sketch.originPoint,
        circle.centerSketchPoint,
        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
        adsk.core.Point3D.create(length_cm / 2.0, -max(width_cm * 0.3, 0.5), 0),
    )
    center_y_dimension = sketch.sketchDimensions.addDistanceDimension(
        sketch.originPoint,
        circle.centerSketchPoint,
        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
        adsk.core.Point3D.create(
            length_cm + max(length_cm * 0.3, 0.5), width_cm / 2.0, 0
        ),
    )
    _set_parameter_expression(bore_dimension, f"{bore_diameter_param} / 2")
    _set_parameter_expression(center_x_dimension, f"{length_param} / 2")
    _set_parameter_expression(center_y_dimension, f"{width_param} / 2")

    profile = _profile_with_loop_count(sketch, 2, component_spec["name"])
    extrude = component.features.extrudeFeatures.addSimple(
        profile,
        adsk.core.ValueInput.createByString(height_param),
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    if not extrude or extrude.bodies.count != 1:
        raise RuntimeError(
            f"Fusion failed to extrude plate {component_spec['name']}."
        )
    extrude.name = f"{component_spec['name']} Extrusion"
    body = extrude.bodies.item(0)
    body.name = component_spec["name"]
    return body, {
        "length": length_param,
        "width": width_param,
        "height": height_param,
        "bore_diameter": bore_diameter_param,
    }


def _create_occurrence_transform(component_spec):
    transform = adsk.core.Matrix3D.create()
    axis = component_spec["axis"]
    rotation = {
        "x": (math.pi / 2.0, adsk.core.Vector3D.create(0, 1, 0)),
        "y": (-math.pi / 2.0, adsk.core.Vector3D.create(1, 0, 0)),
    }.get(axis)
    if rotation and not transform.setToRotation(
        rotation[0],
        rotation[1],
        adsk.core.Point3D.create(0, 0, 0),
    ):
        raise RuntimeError(f"Fusion could not orient component on axis {axis}.")
    origin = component_spec["origin_mm"]
    transform.translation = adsk.core.Vector3D.create(
        origin[0] / 10.0, origin[1] / 10.0, origin[2] / 10.0
    )
    return transform


def _check_body(body, component_spec) -> dict:
    if not body or not body.isValid or not body.isSolid:
        raise RuntimeError(
            f"Generated component {component_spec['name']} is not a valid solid."
        )

    bounds = body.boundingBox
    actual_cm = [
        bounds.maxPoint.x - bounds.minPoint.x,
        bounds.maxPoint.y - bounds.minPoint.y,
        bounds.maxPoint.z - bounds.minPoint.z,
    ]
    dims = component_spec["dimensions_mm"]
    if component_spec["type"] in {"box", "plate_with_bore"}:
        expected_mm = [dims["length"], dims["width"], dims["height"]]
    elif component_spec["type"] in {"cylinder", "annular_cylinder"}:
        diameter_key = (
            "outer_diameter"
            if component_spec["type"] == "annular_cylinder"
            else "diameter"
        )
        diameter = dims[diameter_key]
        expected_mm = [diameter, diameter, dims["height"]]
    else:
        raise RuntimeError(f"Unsupported component type: {component_spec['type']}.")

    actual_mm = [value * 10.0 for value in actual_cm]
    for axis, expected, actual in zip(("x", "y", "z"), expected_mm, actual_mm):
        tolerance_mm = max(0.01, expected * 1e-5)
        if abs(expected - actual) > tolerance_mm:
            raise RuntimeError(
                f"{component_spec['name']} {axis}-extent mismatch: "
                f"expected {expected:g} mm, got {actual:g} mm."
            )

    return {
        "name": component_spec["name"],
        "type": component_spec["type"],
        "axis": component_spec["axis"],
        "solid_valid": True,
        "expected_local_dimensions_mm": expected_mm,
        "expected_world_extents_mm": expected_component_extents_mm(component_spec),
        "measured_local_bounding_box_mm": [round(value, 6) for value in actual_mm],
        "check": "PASS",
    }


def _select_specs(ui) -> list[str]:
    dialog = ui.createFileDialog()
    dialog.title = "Select one or more Fusion model specifications"
    dialog.filter = "JSON model specifications (*.json)"
    dialog.isMultiSelectEnabled = True
    if dialog.showOpen() != adsk.core.DialogResults.DialogOK:
        return []
    return normalize_selected_spec_paths(
        getattr(dialog, "filenames", None),
        getattr(dialog, "filename", None),
    )


def _select_output_folder(ui):
    dialog = ui.createFolderDialog()
    dialog.title = "Choose a folder for the Fusion archive and report"
    if dialog.showDialog() != adsk.core.DialogResults.DialogOK:
        return None
    return dialog.folder


def _generate_one_spec(app, spec_path: str, output_dir: str) -> dict:
    document = None
    try:
        with open(spec_path, "r", encoding="utf-8") as stream:
            spec = validate_model_spec(json.load(stream))

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError("Fusion did not create an active design document.")

        document = app.activeDocument
        if not document:
            raise RuntimeError("Fusion did not create an active document.")
        document.name = spec["design_name"]

        root = design.rootComponent
        component_reports = []

        for index, component_spec in enumerate(spec["components"], start=1):
            transform = _create_occurrence_transform(component_spec)
            occurrence = root.occurrences.addNewComponent(transform)
            component = occurrence.component
            component.name = component_spec["name"]
            parameter_prefix = f"Part{index:02d}"

            if component_spec["type"] == "box":
                body, parameters = _create_box(
                    design, component, component_spec, parameter_prefix
                )
            elif component_spec["type"] == "cylinder":
                body, parameters = _create_cylinder(
                    design, component, component_spec, parameter_prefix
                )
            elif component_spec["type"] == "annular_cylinder":
                body, parameters = _create_annular_cylinder(
                    design, component, component_spec, parameter_prefix
                )
            else:
                body, parameters = _create_plate_with_bore(
                    design, component, component_spec, parameter_prefix
                )

            report = _check_body(body, component_spec)
            report["parameters"] = parameters
            report["origin_mm"] = component_spec["origin_mm"]
            component_reports.append(report)

        base_path = _unique_base(output_dir, safe_file_stem(spec["design_name"]))
        archive_path = base_path + ".f3d"
        export_options = design.exportManager.createFusionArchiveExportOptions(
            archive_path
        )
        if not export_options or not design.exportManager.execute(export_options):
            raise RuntimeError("Fusion could not export the native design archive.")
        if not os.path.isfile(archive_path) or os.path.getsize(archive_path) <= 0:
            raise RuntimeError("Fusion reported success but the .f3d file is missing or empty.")

        report_path = base_path + "-report.json"
        report = {
            "report_version": 1,
            "script_version": SCRIPT_VERSION,
            "status": "EXPORTED_IN_FUSION",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "design_name": spec["design_name"],
            "design_status": spec["design_status"],
            "assumptions": spec["assumptions"],
            "source_spec": os.path.basename(spec_path),
            "units": "mm",
            "coordinate_system": "right-handed, Z-up; component origins are bottom-face origins",
            "native_archive": os.path.basename(archive_path),
            "native_archive_bytes": os.path.getsize(archive_path),
            "native_archive_sha256": _sha256(archive_path),
            "component_count": len(component_reports),
            "components": component_reports,
            "verification": [
                {
                    "check": "Fusion sketch and extrusion created for every component",
                    "status": "PASS",
                },
                {
                    "check": "Solid validity and principal bounding-box dimensions",
                    "status": "PASS",
                },
                {
                    "check": "Component axis placement applied from the model specification",
                    "status": "PASS",
                },
                {
                    "check": "Fusion archive exists and is non-empty",
                    "status": "PASS",
                },
                {
                    "check": "Archive reopened in a separate Fusion session",
                    "status": "NOT RUN",
                },
                {
                    "check": "Strength, safety, fit, and manufacturability",
                    "status": "NOT RUN",
                },
            ],
            "limitations": [
                "This generator supports boxes, cylinders, annular cylinders, and centered-bore plates.",
                "Component axes are limited to the global X, Y, or Z directions.",
                "Inspect component placement and mating interfaces visually in Fusion; no joints or fit checks are generated.",
                "The .f3d archive contains Fusion sketches, dimensions, user parameters, and extrusion features.",
                "A successful export is not engineering approval or manufacturing validation.",
            ],
        }
        with open(report_path, "w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")

        return {
            "source_spec": os.path.basename(spec_path),
            "design_name": spec["design_name"],
            "archive_path": archive_path,
            "report_path": report_path,
        }
    except Exception:
        if document:
            try:
                document.close(False)
            except Exception as close_error:
                raise RuntimeError(
                    f"{traceback.format_exc()}\n"
                    f"Fusion also failed to close the incomplete document: {close_error}"
                ) from close_error
        raise


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        spec_paths = _select_specs(ui)
        if not spec_paths:
            return
        output_dir = _select_output_folder(ui)
        if not output_dir:
            return

        successes = []
        failures = []
        for spec_path in spec_paths:
            try:
                successes.append(_generate_one_spec(app, spec_path, output_dir))
            except Exception as error:
                failures.append(
                    {"source_spec": os.path.basename(spec_path), "error": str(error)}
                )

        lines = [
            f"Finished processing {len(spec_paths)} model specification(s).",
            f"Created {len(successes)} archive(s); {len(failures)} failed.",
            f"Output folder: {output_dir}",
        ]
        for item in successes[:10]:
            lines.append(
                f"Created: {os.path.basename(item['archive_path'])} "
                f"({os.path.basename(item['source_spec'])})"
            )
        if len(successes) > 10:
            lines.append(f"...and {len(successes) - 10} more archive(s).")
        for item in failures[:10]:
            lines.append(f"Failed: {item['source_spec']} — {item['error']}")
        if len(failures) > 10:
            lines.append(f"...and {len(failures) - 10} more failure(s).")
        lines.append(
            "Each selected JSON creates a separate Fusion design. "
            "A JSON containing multiple components remains one design."
        )
        ui.messageBox("\n".join(lines))
    except Exception:
        if ui:
            ui.messageBox(f"Fusion model generation failed:\n\n{traceback.format_exc()}")
