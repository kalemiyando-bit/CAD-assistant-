---
name: mechanical-cad
description: Creates or revises mechanical 3D parts and assemblies for CAD handoff. Use for STEP geometry, robot mechanisms, SolidWorks or AutoCAD-compatible mechanical modeling, and CAD import/export checks.
---

# Mechanical CAD

Follow `.agents/skills/engineering-design-coordinator/SKILL.md` for intake, target software, research scope, tool readiness, ownership, and review. Read the design contract before changing geometry.

## Select a real tool path

- Determine the target application and version. Distinguish neutral geometry delivery from native parametric modeling.
- Check which CAD kernel or application is actually available in the current environment before using it. The default system Python in this project currently lacks CadQuery and ezdxf; do not assume the project's CAD dependencies are installed.
- Smoke-test the selected CAD path with a simple known part and a real export/re-import.
- If the user's target is not accessible, provide a compatible exchange file or a clearly labeled script/macro and instructions. Do not claim a native SolidWorks feature tree from a STEP file.

## Geometry and coordinate rules

- Use millimetres unless the contract states otherwise. Declare the origin and axes in the handoff.
- For robot models in this project, use global Z vertical, X chassis length, and Y chassis width.
- Build from the contract's master dimensions and interface register. Do not silently change agreed interfaces.
- Keep real geometry, simplified purchased-part envelopes, and illustrative geometry distinguishable in names and metadata.
- A CAD solid is not evidence of strength, stability, safe operation, or manufacturability.

## STEP handoff

- STEP is the default neutral format for 3D parts and assemblies.
- For robot CAD handoffs, export STEP files only unless the user asks for additional formats.
- Export separate parts and coordinated assemblies when requested or needed for editing; use consistent, descriptive filenames and revisions.
- STEP does not preserve the source feature tree. If native editable features are required, confirm that the target native application can be operated or provide a clearly marked macro/workflow for the user to run.
- Keep exported deliverables in the requested package, not mixed with temporary meshes, screenshots, or debug files.

## CAD verification

Before handoff, check what the available tools permit:

1. Kernel validity and solid count.
2. Expected bounding box, units, coordinate orientation, and critical dimensions.
3. Part/assembly structure and obvious interferences or missing components.
4. STEP export followed by re-import and comparison of basic dimensions/volume.
5. Human-readable views from the actual model for orientation and assembly/service access.

Record every check as PASS, FAIL, BLOCKED, or NOT RUN with evidence. Do not fix failed checks by loosening a requirement without user approval. Record supplier-dependent envelopes and calculations still needed.

