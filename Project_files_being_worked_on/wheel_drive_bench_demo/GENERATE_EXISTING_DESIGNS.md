# Generate the current wheel-drive parts in Fusion

## Current source package

Use the existing Fusion model generator, version **1.3.0**, from
`Project_files_being_worked_on/fusion_native_pilot/`. Copy the entire folder to
a stable location on the Windows computer running Fusion. Do not copy only the
`generate_fusion_model/` child folder; the script loads shared code from the
parent.

In Fusion, open **Tools → Scripts and Add-Ins**, choose **Add Script from
device**, and select the `generate_fusion_model/` child folder inside the copied
`fusion_native_pilot/`. The script keeps the same name and folder for this
project; do not create a new script entry for each part.

## Part specifications

These are the three current, separate part specifications:

1. Shaft POC-02:
   `shaft_3d_POC02/wheel_drive_shaft_POC02_model_spec.json`
2. Wheel rim POC-03:
   `wheel_rim_3d_POC03/wheel_rim_POC03_model_spec.json`
3. Hub POC-04:
   `hub_3d_POC04/hub_POC04_model_spec.json`

Copy the JSON files to a folder accessible to Fusion. Run **Generate Fusion
Model from JSON**, then select one specification or multi-select several. One
selected JSON creates one Fusion design; a JSON containing several components
still creates one multi-component design. When multiple JSON files are selected,
the add-in creates a separate `.f3d` archive and report for each one. Existing
output filenames are not overwritten; a numbered suffix is used.

Do **not** select the parent `preliminary_wheel_drive_spec.json` for this
individual-part run. It is a seven-component exploratory concept, not a
reviewed assembly. The older `shaft_2d_test/shaft_6x46_A0_model_spec.json` is
also not the current shaft handoff.

## Output folder

The generator writes to the user-configured folder:

`C:\Users\mweny\Documents\3D_DESIGNS\FUSION_26\CAD_Assistant\wheel_drive_bench_demo\GENERATED`

The add-in creates this directory if it does not exist and no longer prompts
for an output folder on each run. To change the location later, update
`DEFAULT_OUTPUT_FOLDER` in
`Project_files_being_worked_on/fusion_native_pilot/generate_fusion_model.py`
once, then refresh the existing script package in Fusion.

## Progress and verification status

- Local focused model-spec and batch-selection tests: **27 passed**.
- Python syntax checks: **passed**.
- Script and manifest versions agree at **1.3.0**.
- The configured output path matches the user-provided location.
- Autodesk Fusion is not available in this Replit environment. The user
  previously reported successful shaft generation with the earlier installed
  version, but has deleted that add-in. The fresh 1.3.0 install, multi-file
  selection, and fixed output-folder behavior have not yet been confirmed in
  Fusion.
- Keep generated dimensions preliminary. The user asked to defer combined
  design verification until all planned parts are created.

## Future assembly capability

The current command creates separate Fusion designs from model-spec JSON files.
A single JSON can describe several primitive components with axis-aligned
placement, but the generator does not import the separate `.f3d` part archives
or create joints, clearances, or fit relationships. A future assembly workflow
can be added to this same script package, using reviewed part references and an
assembly specification for placements and joints. Do not treat the existing
seven-component concept JSON as a validated assembly.
