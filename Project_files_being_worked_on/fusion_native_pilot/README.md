# Fusion-native pilot

This is the first executable CAD handoff path for the conversational,
Skill-driven CAD Assistant. It does not use an external API key or a separate
AI service. The assistant can prepare a validated JSON model specification;
Autodesk Fusion runs the supplied script and creates the native design.

## Included

- `generate_fusion_model.py` — creates native Fusion components from JSON using
  sketches, driving dimensions, user parameters, and extrusion features.
- `convert_step_to_fusion_archive.py` — imports a STEP file and saves the
  imported design as a Fusion `.f3d` archive.
- `fusion_model_spec.py` — dependency-free schema validation used by the model
  generator and its tests.
- `example_model_spec.json` — a 100 × 60 × 40 mm rectangular-block smoke test,
  matching the existing neutral-format test geometry.

## Run the native model generator

1. Copy this folder to a location where Fusion can access it.
2. In Fusion, open **Tools → Scripts and Add-Ins** and add this folder as a
   script location.
3. Run **Generate Fusion Model from JSON**.
4. Select `example_model_spec.json`, then choose an output folder.
5. Open the resulting `.f3d` file in Fusion and inspect the component, sketch,
   driving dimensions, user parameters, and extrusion in the timeline.
6. Review the adjacent `-report.json`; it records dimensions, checks, and
   SHA-256 for the archive.

The model generator currently supports right-handed, Z-up millimetre models
made from box and cylinder base features. It deliberately rejects unsupported
features rather than silently approximating them.

## Run the STEP archive handoff

1. In Fusion's **Scripts and Add-Ins**, run **Import STEP to Fusion Archive**.
2. Select a STEP file and an output folder.
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
is not installed in the Replit environment, so execution of the Fusion API
scripts and inspection of the resulting `.f3d` remain blocked until they are run
inside the user's Fusion installation.

## Engineering limits

- This is a tool-path and file-format pilot, not a validated robot design.
- A valid solid and successful archive export do not demonstrate strength,
  safety, clearances, fit, compliance, or manufacturing readiness.
- For every real design, the coordinator still records the target software and
  version, research scope, requirements, interfaces, assumptions, and checks.
