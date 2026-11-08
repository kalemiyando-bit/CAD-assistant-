# Engineering Workflow Playbook

This is the project-specific map of implementation paths for other agents.
Use it with the engineering-design coordinator and the relevant discipline
Skills; it does not replace the user's design contract or prove that an
application-level workflow has succeeded.

## Current wheel-drive test order

The user's requested system test is deliberately incremental:

1. Create a 2D drawing for one simple part and have the user import it into
   Fusion.
2. After the 2D handoff is reviewed, create the matching 3D part and review it
   in Fusion.
3. Continue with other parts, then the assembly.
4. Develop the safety/control design and PCB after the mechanical and
   electrical requirements are established.

Do not skip ahead to a full assembly, powered test, or PCB layout to make the
first workflow demonstration look more complete. A clearly labeled draft is
useful; unsupported production claims are not.

The shaft example has since been reported as producing both a 2D drawing and a
3D model, with tests passing. It is a workflow demonstrator only; the engineering
assistant is not limited to shafts.

## Efficient verification

Do not run a full test suite for every design iteration. For a generated CAD
deliverable, first have the user inspect/import it in the target application.
If it fails to load or import, run focused diagnostics and tests for that
failure rather than repeating unrelated suites. Preserve task-specific safety
or release checks agreed in the design contract. A successful import does not
prove dimensional accuracy, fit, strength, safety, or manufacturing readiness.

## Start each design task

1. Read `.agents/skills/engineering-design-coordinator/SKILL.md`, the current
   design contract, and the matching mechanical, drawing, or PCB Skill.
2. Reuse answers already recorded in the current conversation and contract.
   For a new design task, confirm the target CAD/EDA software and version when
   they affect the handoff. Do not imply Replit can operate a desktop program
   unless an actual connection exists.
3. For any 2D deliverable, ask whether it is a model-building sketch, a
   documentation drawing, or both. If both, make separate outputs. Model
   sketches contain only the profiles/construction geometry needed for 3D work;
   documentation sheets contain dimensions and title-block details.
4. Record requirements, deliverables, coordinate frame, units, known interfaces,
   open questions, and research scope in the contract. Current wheel-drive
   research scope is **user sources only**; do not broaden it without asking.
5. Use one current source for dimensions. In the wheel-drive pilot that source is
   `Project_files_being_worked_on/wheel_drive_bench_demo/preliminary_wheel_drive_spec.json`.
   Keep assumptions visible and do not turn them into approved dimensions.
6. Give each shared output one writer. Reviewers report findings without
   silently editing specialist-owned deliverables.

## 2D drawing handoff — current first test

### Implementation

- The single-part example is the plain drive-shaft envelope from the A0 concept:
  diameter 6 mm, length 46 mm, axis +Y. Both dimensions are provisional.
- Choose the output purpose before running the generator. The CLI requires an
  explicit choice:

  ```sh
  python Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/generate_shaft_drawing.py --purpose model-sketch
  python Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/generate_shaft_drawing.py --purpose documentation
  ```

- The script reads and validates the shaft component from
  `preliminary_wheel_drive_spec.json`. It reuses the project's standard-library
  `DxfWriter` in `wheel_drive_bench_demo/generate_preliminary_dxf.py`.
  `--purpose model-sketch` writes
  `shaft_2d_test/shaft_6x46_A0_model_profile_R12.dxf`, containing only a Ø6 mm
  circle profile. The separate dimension schedule gives a provisional 46 mm
  extrusion length; for a +Y shaft axis, sketch on XZ and extrude in +Y.
  `--purpose documentation` writes:
  - `shaft_2d_test/shaft_6x46_A0_R12_retry.dxf` — minimal R12 ASCII DXF in
    millimetres, with side and end views, dimensions, notes, and sheet details.
  - `shaft_2d_test/shaft_6x46_A0_preview.html` — self-contained SVG preview with
    a DXF download link.
- The original AC1015 attempt (`shaft_6x46_A0.dxf`) failed to insert in Fusion
  2026 with the generic message “DXF file failed to insert.” It is retained for
  comparison only. The user later confirmed that the R12 documentation retry
  inserted successfully; the Fusion version for that successful import was not
  recorded.
- In the successful import, the user observed that the border, title-block
  space, and dimension graphics also appeared as sketch geometry. This is
  expected: DXF annotations are ordinary entities, not associative Fusion
  dimensions, and an inserted documentation sheet is not a native drawing.
- Do not use the full documentation sheet as a modeling sketch unless the user
  explicitly wants its frame and annotations as geometry. Ask the intended
  purpose first; keep model profiles and documentation sheets separate.

### Checks and evidence

The local drawing tests are available when diagnosing a failed or malformed
output, or when requested. Avoid rerunning the full suite during routine design
iterations. If needed, run the focused local drawing tests with:

```sh
python -m unittest discover -s Project_files_being_worked_on/wheel_drive_bench_demo/tests -v
```

The local suite checks the preliminary concept DXF and the shaft generator's
source dimensions, R12 header, millimetre units, documentation views/labels, and
that the model-sketch DXF contains only its profile circle. These checks do
**not** test Fusion's DXF importer or verify the imported scale and placement.

The user now reports that the shaft example's tests passed and that it can
produce both a 2D drawing and a 3D model. The earlier record confirms basic
import of the documentation DXF into Fusion. The exact checks covered by the
newer report have not yet been itemized here; confirm whether it included the
model-sketch DXF's single-profile import, scale, and extrusion-axis checks.
Record the Fusion version and any import prompts when known. A local DXF parser
check is not evidence of target-application importability.

If a future request requires a native Fusion drawing sheet, create it from the
reviewed 3D design only after the Fusion drawing workflow has itself been
smoke-tested. Do not describe the current DXF as a native drawing.

## 3D mechanical handoff — multi-spec generator updated; Fusion checks pending

For the wheel-drive user's current Fusion setup and the three available
part-level specifications, see
`Project_files_being_worked_on/wheel_drive_bench_demo/GENERATE_EXISTING_DESIGNS.md`.
The combined local review for POC-02 through POC-08 is recorded in
`Project_files_being_worked_on/wheel_drive_bench_demo/REVIEW_POC02-08_LOCAL.md`.

### Simple native Fusion geometry

1. Use the contract and the dimension schedule to create a version-1 JSON model
   specification. For the first shaft test, make it a **one-component**
   specification; do not submit the seven-part wheel-drive specification when
   the user asked to test one part.
   The current one-part test spec is
   `Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/shaft_6x46_A0_model_spec.json`;
   it defines a provisional Ø6 mm × 46 mm cylinder aligned to +Y at the origin.
2. Follow
   `Project_files_being_worked_on/fusion_native_pilot/README.md` and validate
   the JSON with `fusion_model_spec.py`.
3. The current schema accepts millimetre, right-handed Z-up models containing
   `box`, `cylinder`, `annular_cylinder`, and `plate_with_bore` components.
   Component axes can align to X, Y, or Z. It does not encode assembly joints,
   fits, materials, clearances, or interference results.
4. Run the existing Fusion script **inside Autodesk Fusion**:
   `Project_files_being_worked_on/fusion_native_pilot/generate_fusion_model/`.
   In Fusion, add that child folder through **Tools → Scripts and Add-Ins**,
   choose **Generate Fusion Model from JSON**, and select one or more one-part
   JSON specifications. Each selected specification creates a separate design
   and `.f3d` archive. The script saves to its configured default output folder,
   creating it if needed; it does not show an output-folder prompt.
5. Inspect the generated `.f3d` and adjacent report in Fusion. Check units,
   component count, axis orientation, critical dimensions, sketches, parameters,
   and extrusions. Reopen the archive in another Fusion session before claiming
   that archive-open check passed.

### Proven versus pending

- The focused local model-spec and batch-selection suites currently have 28
  passing tests:

  ```sh
  python -m unittest discover -s Project_files_being_worked_on/fusion_native_pilot/tests -p 'test_fusion*.py' -v
  ```

- These tests validate JSON normalization/rejection and multi-file selection
  helpers. They do **not** execute the Autodesk Fusion API.
- The user now reports that the shaft example tests passed and both 2D and 3D
  outputs can be created. The earlier note that Fusion execution was pending is
  superseded for that reported capability, but the exact Fusion-side checks have
  not yet been recorded. Confirm whether the generator ran inside Fusion, the
  `.f3d` opened, and the shaft's units, dimensions, and +Y axis were inspected
  before marking those specific checks complete.
- The user deleted their prior local add-in and asked to start from a fresh
  installation. The current project package is version 1.3.0; the user has not
  yet reported installing or running this version in Fusion.
- Batch selection in Fusion and automatic creation/use of the configured local
  output directory are not yet confirmed in the desktop application. The output
  location is set in `generate_fusion_model.py`.
- Y-axis placement for the other supported features and annular/bored geometry
  still need their own Fusion smoke tests.
- The model generator's success report is not proof of fit, strength, safety, or
  manufacturing readiness.

For geometry that cannot be built with the supported simple features, a
separate script can import a verified STEP file into Fusion and save an `.f3d`
archive. Imported STEP geometry does not regain the source model's parametric
feature history. Use STEP only when it is the right handoff, and state that
limitation.

## PCB and electrical-control handoff — procedure only, not yet proven here

Use `.agents/skills/pcb-design/SKILL.md`; do not assume KiCad or Fusion
Electronics. Before creating a schematic or board, establish:

- EDA application and version, and whether the requested result is a concept
  schematic, editable native project, routed board, fabrication files, or
  mechanical-fit model.
- Motor and controller part numbers, supply range, load/current estimates,
  control inputs and states, connectors, board/enclosure limits, and stop
  behavior.
- The permitted research scope and source evidence for pinouts, ratings,
  protection, and thermal limits.

The wheel-drive A0 contract lists the Mabuchi FF-130 motor and DRV8833 only as
candidates. Neither is selected, and no PCB or firmware exists. Do not design
around candidate ratings as if they were confirmed requirements.

The current contract records that Fusion Electronics' public API cannot create
or edit board content. If Fusion Electronics is selected, native board editing
must use its UI unless an import route is separately verified. For another
EDA, first check tool availability and smoke-test a harmless open/export/check
operation. No PCB authoring path has been proven in this project yet.

After a draft, run the available schematic/ERC, netlist, PCB/DRC, and
manufacturer-rule checks. Preserve warnings and human-review needs. Do not call
the board fabrication-ready because a tool reports zero errors.

## Safety and powered-test boundary

The current wheel-drive concept is not approved for powered testing. Its A0
notes calculate about 31 m/s rim speed from an 80 mm wheel and the unselected
motor candidate's listed 7,400 rpm no-load speed. This is a calculation, not a
measured operating speed. A speed limit, physical guard, current-limited bench
procedure, and defined stop behavior remain necessary before any powered test.
The existing candidate is not evidence that the motor is suitable.

## Current evidence ledger

| Area | Locally checked | Still pending |
|---|---|---|
| Shaft 2D test | DXF/HTML generated; eight project drawing tests pass | User's Fusion import, scale, and annotation review |
| Simple 3D model | 28 focused local tests pass; all seven wheel-drive part specs validate locally; one/many JSON generation is implemented | Fresh v1.3.0 install, batch run, output-folder creation, Fusion inspection, and archive reopen |
| Assembly | A seven-envelope preliminary spec exists; generator can create multiple placed components from one spec | Import/link reviewed part archives, define joints and interfaces, and verify the Fusion assembly/archive workflow |
| PCB/control | Requirements and candidate parts are documented | EDA choice, selected parts, schematic, board, firmware, and checks |
| Safety | High candidate rim-speed concern is documented | Guard, speed limit, stop/control requirements, and powered-test procedure |

`wheel_drive_bench_demo/REVIEW_A0.md` is the original non-independent concept
review. Its finding that no drawing was included predates the later shaft 2D
workflow test; it has not been replaced by a new engineering review.
