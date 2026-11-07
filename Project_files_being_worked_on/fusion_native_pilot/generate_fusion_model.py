"""Create native Fusion sketch-and-extrude components from a JSON model spec.

Run this script inside Autodesk Fusion from Tools > Scripts and Add-Ins.
The output is an F3D archive containing Fusion-native component sketches,
dimensions, user parameters, and extrusion features.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import traceback
from datetime import datetime, timezone

import adsk.core
import adsk.fusion


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from fusion_model_spec import safe_file_stem, validate_model_spec


SCRIPT_VERSION = "1.0.1"


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
    if component_spec["type"] == "box":
        expected_mm = [dims["length"], dims["width"], dims["height"]]
    else:
        expected_mm = [dims["diameter"], dims["diameter"], dims["height"]]

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
        "solid_valid": True,
        "expected_dimensions_mm": expected_mm,
        "measured_bounding_box_mm": [round(value, 6) for value in actual_mm],
        "check": "PASS",
    }


def _select_spec(ui):
    dialog = ui.createFileDialog()
    dialog.title = "Select a Fusion model specification"
    dialog.filter = "JSON model specifications (*.json)"
    dialog.isMultiSelectEnabled = False
    if dialog.showOpen() != adsk.core.DialogResults.DialogOK:
        return None
    return dialog.filename


def _select_output_folder(ui):
    dialog = ui.createFolderDialog()
    dialog.title = "Choose a folder for the Fusion archive and report"
    if dialog.showDialog() != adsk.core.DialogResults.DialogOK:
        return None
    return dialog.folder


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        spec_path = _select_spec(ui)
        if not spec_path:
            return
        output_dir = _select_output_folder(ui)
        if not output_dir:
            return

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
            transform = adsk.core.Matrix3D.create()
            origin = component_spec["origin_mm"]
            transform.translation = adsk.core.Vector3D.create(
                origin[0] / 10.0, origin[1] / 10.0, origin[2] / 10.0
            )
            occurrence = root.occurrences.addNewComponent(transform)
            component = occurrence.component
            component.name = component_spec["name"]
            parameter_prefix = f"Part{index:02d}"

            if component_spec["type"] == "box":
                body, parameters = _create_box(
                    design, component, component_spec, parameter_prefix
                )
            else:
                body, parameters = _create_cylinder(
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
                "This generator supports only box and cylinder base features.",
                "The .f3d archive contains Fusion sketches, dimensions, user parameters, and extrusion features.",
                "A successful export is not engineering approval or manufacturing validation.",
            ],
        }
        with open(report_path, "w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")

        ui.messageBox(
            "Fusion model created.\n\n"
            f"Native archive: {archive_path}\n"
            f"Generation report: {report_path}\n\n"
            "Review the feature timeline and report before using the model."
        )
    except Exception:
        if ui:
            ui.messageBox(f"Fusion model generation failed:\n\n{traceback.format_exc()}")
