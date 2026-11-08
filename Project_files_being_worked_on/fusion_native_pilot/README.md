# Fusion-native pilot

This is the first executable CAD handoff path for the conversational,
Skill-driven CAD Assistant. The Fusion generator itself does not use an external
API key or AI service. An optional, separate Gemini CLI worker can draft a
validated JSON model specification; Autodesk Fusion runs the supplied script
and creates the native design.

## Included

- `generate_fusion_model.py` — creates native Fusion components from JSON using
  sketches, driving dimensions, user parameters, and extrusion features.
- `convert_step_to_fusion_archive.py` — imports a STEP file and saves the
  imported design as a Fusion `.f3d` archive.
- `fusion_model_spec.py` — dependency-free schema validation used by the model
  generator and its tests.
- `gemini_part_spec_worker.py` — optional server-side CLI that sends only an
  explicitly supplied single-part brief to Gemini and validates the result.
- `example_model_spec.json` — a 100 × 60 × 40 mm rectangular-block smoke test,
  matching the existing neutral-format test geometry.

## Run the native model generator

1. Copy this entire folder to a location where Fusion can access it. Keep each
   named script folder inside `fusion_native_pilot`; the entry points load their
   shared implementation and validator from this parent folder.
2. In Fusion, open **Tools → Scripts and Add-Ins**, choose **Add Script from
   device**, and select the `generate_fusion_model/` child folder (not the
   `fusion_native_pilot/` parent).
3. Run **Generate Fusion Model from JSON**.
4. In the file picker, select one JSON model specification or multi-select
   several JSON files, then choose one output folder. Selecting one file keeps
   the original one-at-a-time workflow.
5. The add-in creates a separate Fusion design, `.f3d` archive, and adjacent
   `-report.json` for each selected specification. A single specification with
   several components still creates one combined design. If one specification
   fails, the add-in continues with the rest and reports each result.
6. Open each resulting `.f3d` file in Fusion and inspect the component, sketch,
   driving dimensions, user parameters, and extrusion in the timeline.
7. Review each adjacent `-report.json`; it records dimensions, checks, and
   SHA-256 for the archive.

The shaft test spec creates one provisional straight cylinder: Ø6 mm × 46 mm,
aligned with global +Y and based at the origin. It creates a Fusion-native
sketch, driving dimensions, user parameters, and extrusion, then exports an
`.f3d` archive. These dimensions are for the workflow test only and are not
approved for manufacture.

The model generator currently supports right-handed, Z-up millimetre models
made from boxes, cylinders, annular cylinders, and centered-bore plates.
Components can be aligned to global X, Y, or Z. The supported geometry remains
limited to simple extruded profiles; unsupported features are rejected rather
than silently approximated. Component placement is by translation and axis
alignment only; joints, materials, clearances, and interference checks are not
generated. X/Y-oriented parts, annular profiles, and bored plates need a Fusion
smoke test before they can be treated as verified.

## Run the STEP archive handoff

1. In Fusion's **Scripts and Add-Ins**, choose **Add Script from device** and
   select the `convert_step_to_fusion_archive/` child folder.
2. Run **Import STEP to Fusion Archive**, then select a STEP file and output
   folder.
3. Open the resulting `.f3d` file and review the source units, coordinate frame,
   body count, and critical dimensions against the design contract.

The `.f3d` is a native Fusion archive, but imported STEP bodies do **not** regain
the original CAD application's parametric feature history. The report marks
dimension review and reopening in a second Fusion session as `NOT RUN`.

## Local checks

From the workspace root:

```sh
python -m unittest discover -s Project_files_being_worked_on/fusion_native_pilot/tests -v
python -m py_compile Project_files_being_worked_on/fusion_native_pilot/fusion_model_spec.py Project_files_being_worked_on/fusion_native_pilot/generate_fusion_model.py Project_files_being_worked_on/fusion_native_pilot/convert_step_to_fusion_archive.py
```

These checks validate the JSON contract and Python syntax only. Autodesk Fusion
is not installed in the Replit environment. The user now reports that the shaft
example's tests passed and it can produce a 3D model, but this README does not
record the Fusion version or whether the resulting `.f3d` was opened and its
dimensions and axis inspected. X/Y-oriented variants and annular/bored profiles
still need their own Fusion smoke tests before being treated as verified.

Version 1.2.0 adds multi-selection of JSON model specifications in the existing
`generate_fusion_model` script. It does not require a separate add-in for each
part; update the existing script package once to use the batch feature.

## Engineering limits

- This is a tool-path and file-format pilot, not a validated robot design.
- A valid solid and successful archive export do not demonstrate strength,
  safety, clearances, fit, compliance, or manufacturing readiness.
- For every real design, the coordinator still records the target software and
  version, research scope, requirements, interfaces, assumptions, and checks.
