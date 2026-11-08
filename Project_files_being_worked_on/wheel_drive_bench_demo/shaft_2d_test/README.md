# Shaft 2D workflow test — A0

This is the first single-part drafting test for the Wheel Drive Bench
Demonstrator.

## Files

- `shaft_6x46_A0_model_profile_R12.dxf` — one circle profile only, for creating
  the shaft as a 3D feature.
- `shaft_6x46_A0_R12_retry.dxf` — full documentation sheet in minimal R12 ASCII
  DXF format, including views, dimensions, notes, and a sheet frame.
- `shaft_6x46_A0_preview.html` — self-contained preview and download link for
  the documentation DXF.
- `generate_shaft_drawing.py` — generates either purpose from the shaft entry
  in `../preliminary_wheel_drive_spec.json`; a purpose must be selected.

Run one of these after confirming the user's intended purpose:

```sh
python Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/generate_shaft_drawing.py --purpose model-sketch
python Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/generate_shaft_drawing.py --purpose documentation
```

## Design status

The part is a plain cylindrical envelope, diameter 6 mm by length 46 mm, with
its axis along +Y. These are provisional values copied from the A0 concept
specification for testing the design workflow. They are not confirmed component
dimensions. End shape, material, tolerance, finish, and retention features are
not specified. This drawing is not for manufacture.

The first AC1015/AutoCAD 2000 DXF attempt (`shaft_6x46_A0.dxf`) failed to insert
in the user's Fusion installation and is retained only for comparison. The
minimal R12 retry has since been inserted successfully by the user; the Fusion
version for that successful import was not recorded.

## Fusion import test

The user confirmed that the documentation DXF inserted, and observed that the
sheet border, title-block space, dimension graphics, and notes also appeared as
sketch geometry. This is expected: DXF entities do not become native Fusion
drawing annotations or associative dimensions. The import check confirms basic
R12 compatibility, but scale, placement, and text legibility were not reported.

For the model-building sketch:

1. Open a new Fusion design and create a sketch on the plane normal to the shaft
   axis (use XZ if preserving the specified +Y axis).
2. Use **Insert DXF**, select `shaft_6x46_A0_model_profile_R12.dxf`, and keep
   the import units in millimetres.
3. Finish the sketch and inspect the single Ø6 mm circle. Extrude it 46 mm in
   +Y to create the provisional cylindrical envelope.

Do not insert the full documentation sheet DXF into a modeling sketch unless the
user deliberately wants its sheet and annotation linework there. A native
Fusion drawing-sheet workflow has not been verified in this project.

## 3D shaft test

- `shaft_6x46_A0_model_spec.json` is a one-component Fusion model specification
  for the same provisional Ø6 mm × 46 mm cylinder, with its axis along +Y.
- `shaft_6x46_A0_fusion_native_bundle.zip` contains that specification and the
  Fusion-native model generator. Extract the ZIP while preserving its folders.
- In Fusion, add
  `fusion_native_pilot/generate_fusion_model/` through **Tools → Scripts and
  Add-Ins → Add Script from device**. Run **Generate Fusion Model from JSON**,
  select the shaft model spec, and choose an output folder.
- Fusion should create a native `.f3d` and a report JSON. The user now reports
  that the shaft example's tests passed and that it can produce a 3D model.
  This README does not yet record the Fusion version or whether the generated
  archive was opened and its dimensions and axis inspected; see
  `ENGINEERING_WORKFLOW_PLAYBOOK.md` for the current evidence status.
