"""Import one STEP file into Fusion and export the design as a native F3D archive.

Run inside Fusion from Tools > Scripts and Add-Ins. Imported STEP solids remain
boundary-representation geometry; this does not recreate the original feature tree.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import traceback
from datetime import datetime, timezone

import adsk.core
import adsk.fusion


SCRIPT_VERSION = "1.0.0"


def _safe_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return stem[:80] or "fusion-import"


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


def _select_step(ui):
    dialog = ui.createFileDialog()
    dialog.title = "Select the STEP file to import"
    dialog.filter = "STEP files (*.step; *.stp)"
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


def _geometry_counts(design):
    body_count = 0
    solid_count = 0
    for component in design.allComponents:
        for index in range(component.bRepBodies.count):
            body = component.bRepBodies.item(index)
            body_count += 1
            if body.isSolid:
                solid_count += 1
    return body_count, solid_count


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        step_path = _select_step(ui)
        if not step_path:
            return
        output_dir = _select_output_folder(ui)
        if not output_dir:
            return

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError("Fusion did not create an active design document.")

        import_options = app.importManager.createSTEPImportOptions(step_path)
        if not import_options:
            raise RuntimeError("Fusion could not create STEP import options.")
        imported = app.importManager.importToTarget(
            import_options, design.rootComponent
        )
        if not imported:
            raise RuntimeError("Fusion reported that STEP import failed.")

        body_count, solid_count = _geometry_counts(design)
        if body_count == 0 or solid_count == 0:
            raise RuntimeError(
                "The import completed but no solid bodies were found in the design."
            )

        source_stem = os.path.splitext(os.path.basename(step_path))[0]
        base_path = _unique_base(
            output_dir, _safe_stem(f"{source_stem}-fusion-archive")
        )
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
            "source_step": os.path.basename(step_path),
            "source_step_bytes": os.path.getsize(step_path),
            "source_step_sha256": _sha256(step_path),
            "native_archive": os.path.basename(archive_path),
            "native_archive_bytes": os.path.getsize(archive_path),
            "native_archive_sha256": _sha256(archive_path),
            "imported_bodies": body_count,
            "imported_solid_bodies": solid_count,
            "units": "Confirm against the source contract and Fusion document settings.",
            "coordinate_frame": "Preserved from STEP import; confirm against the source contract.",
            "verification": [
                {"check": "STEP imported by Fusion API", "status": "PASS"},
                {
                    "check": "At least one solid body is present",
                    "status": "PASS",
                },
                {
                    "check": "Fusion archive exists and is non-empty",
                    "status": "PASS",
                },
                {
                    "check": "Imported bounds and critical dimensions checked",
                    "status": "NOT RUN",
                },
                {
                    "check": "Archive reopened in a separate Fusion session",
                    "status": "NOT RUN",
                },
            ],
            "limitations": [
                "The F3D archive is native Fusion format, but imported STEP bodies do not regain the source application's parametric feature history.",
                "This script checks that Fusion imported solids and wrote an archive; it does not validate engineering intent, dimensions, clearances, strength, safety, or manufacturability.",
            ],
        }
        with open(report_path, "w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")

        ui.messageBox(
            "STEP imported and archived in Fusion.\n\n"
            f"Native archive: {archive_path}\n"
            f"Generation report: {report_path}\n\n"
            "The archive contains imported geometry, not the source feature history. "
            "Review units and critical dimensions in Fusion."
        )
    except Exception:
        if ui:
            ui.messageBox(f"STEP-to-Fusion export failed:\n\n{traceback.format_exc()}")
