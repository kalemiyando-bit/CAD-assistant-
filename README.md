# CAD Assistant

A conversational, Skill-driven engineering design workflow for the user's own
mechanical CAD, technical drawing, PCB, and related engineering work. Autodesk
Fusion is the planned primary CAD target, while other tools remain supported.

## Start a design task

Use `.agents/skills/engineering-design-coordinator/SKILL.md` as the entry point.
The coordinator records the design contract, software/version, research scope,
deliverables, requirements, interfaces, assumptions, and verification gates
before substantial design work.

For the concrete 2D, Fusion 3D, and PCB implementation paths—and their current
verification status—see `ENGINEERING_WORKFLOW_PLAYBOOK.md`.

## Fusion-native pilot

`Project_files_being_worked_on/fusion_native_pilot/` contains a validated model
specification, a Fusion API generator for simple native box, cylinder, annular,
and bored-plate features, and a separate STEP-import-to-F3D workflow. Both
Fusion scripts must be run inside Autodesk Fusion. See its README for setup,
limitations, and checks.

`Project_files_being_worked_on/wheel_drive_bench_demo/` contains the current
preliminary wheel-drive concept, its assumptions, and a model specification.
It is exploratory geometry only; dimensions, interfaces, powered operation, and
electrical controls remain unapproved.

## Local validation

```sh
python -m unittest discover -s Project_files_being_worked_on/fusion_native_pilot/tests -v
python -m py_compile Project_files_being_worked_on/fusion_native_pilot/fusion_model_spec.py Project_files_being_worked_on/fusion_native_pilot/generate_fusion_model.py Project_files_being_worked_on/fusion_native_pilot/convert_step_to_fusion_archive.py
pnpm run typecheck
```

Local checks cannot replace running the Fusion scripts and opening the resulting
`.f3d` files in Autodesk Fusion.
