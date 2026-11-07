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

## Start each design task

1. Read `.agents/skills/engineering-design-coordinator/SKILL.md`, the current
   design contract, and the matching mechanical, drawing, or PCB Skill.
2. Reuse answers already recorded in the current conversation and contract.
   For a new design task, confirm the target CAD/EDA software and version when
   they affect the handoff. Do not imply Replit can operate a desktop program
   unless an actual connection exists.
3. Record requirements, deliverables, coordinate frame, units, known interfaces,
   open questions, and research scope in the contract. Current wheel-drive
   research scope is **user sources only**; do not broaden it without asking.
4. Use one current source for dimensions. In the wheel-drive pilot that source is
   `Project_files_being_worked_on/wheel_drive_bench_demo/preliminary_wheel_drive_spec.json`.
   Keep assumptions visible and do not turn them into approved dimensions.
5. Give each shared output one writer. Reviewers report findings without
   silently editing specialist-owned deliverables.

## 2D drawing handoff — current first test

### Implementation

- The single-part example is the plain drive-shaft envelope from the A0 concept:
  diameter 6 mm, length 46 mm, axis +Y. Both dimensions are provisional.
- Run:

  ```sh
  python Project_files_being_worked_on/wheel_drive_bench_demo/shaft_2d_test/generate_shaft_drawing.py
  ```

- The script reads and validates the shaft component from
  `preliminary_wheel_drive_spec.json`. It reuses the project's standard-library
  `DxfWriter` in `wheel_drive_bench_demo/generate_preliminary_dxf.py` and writes:
  - `shaft_2d_test/shaft_6x46_A0.dxf` — editable millimetre DXF, with side and
    end views, dimensions, notes, and a sheet frame.
  - `shaft_2d_test/shaft_6x46_A0_preview.html` — self-contained SVG preview with
    a DXF download link.
- The dimension labels in the DXF are ordinary 2D geometry/text, not
  associative Fusion dimensions. The sheet imports as sketch geometry; it does
  not become a native Fusion drawing sheet.

### Checks and evidence

Run the local drawing tests with:

```sh
python -m unittest discover -s Project_files_being_worked_on/wheel_drive_bench_demo/tests -v
```

The current eight tests pass. They check the preliminary concept DXF and the
shaft generator's source dimensions, millimetre units, views, labels, and
preview SVG. These checks do **not** test Fusion's DXF importer.

The remaining application check is for the user to import the DXF in Fusion,
keep units in millimetres, and inspect view placement, scale, and text. Record
the Fusion version and any import prompts or missing annotations. Do not reuse
this import route for other parts until that review is received.

If a future request requires a native Fusion drawing sheet, create it from the
reviewed 3D design only after the Fusion drawing workflow has itself been
smoke-tested. Do not describe the current DXF as a native drawing.

## 3D mechanical handoff — available path, Fusion execution pending

### Simple native Fusion geometry

1. Use the contract and the dimension schedule to create a version-1 JSON model
   specification. For the first shaft test, make it a **one-component**
   specification; do not submit the seven-part wheel-drive specification when
   the user asked to test one part.
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
   choose **Generate Fusion Model from JSON**, select the one-part JSON, and
   choose an output folder.
5. Inspect the generated `.f3d` and adjacent report in Fusion. Check units,
   component count, axis orientation, critical dimensions, sketches, parameters,
   and extrusions. Reopen the archive in another Fusion session before claiming
   that archive-open check passed.

### Proven versus pending

- The local schema suite currently has 18 passing tests:

  ```sh
  python -m unittest discover -s Project_files_being_worked_on/fusion_native_pilot/tests -v
  ```

- Those tests validate JSON normalization and rejection cases. They do **not**
  execute the Autodesk Fusion API.
- No native Fusion output from the wheel-drive pilot has yet been run and
  inspected in the user's Fusion. Y-axis placement and annular/bored geometry
  still need a Fusion smoke test.
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
| Simple 3D model | JSON schema suite passes; generator and report path are documented | Run generator inside Fusion; inspect and reopen `.f3d` |
| Assembly | A seven-envelope preliminary spec exists | Real part interfaces, joints, clearances, fits, and assembly review |
| PCB/control | Requirements and candidate parts are documented | EDA choice, selected parts, schematic, board, firmware, and checks |
| Safety | High candidate rim-speed concern is documented | Guard, speed limit, stop/control requirements, and powered-test procedure |

`wheel_drive_bench_demo/REVIEW_A0.md` is the original non-independent concept
review. Its finding that no drawing was included predates the later shaft 2D
workflow test; it has not been replaced by a new engineering review.
