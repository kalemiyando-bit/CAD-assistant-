---
name: mechanical-cad
description: Creates or revises mechanical 3D parts and assemblies for CAD handoff. Use for Fusion, STEP geometry, robot mechanisms, SolidWorks or AutoCAD-compatible mechanical modeling, and CAD import/export checks.
---

# Mechanical CAD

Follow `.agents/skills/engineering-design-coordinator/SKILL.md` for intake, target software, research scope, tool readiness, ownership, and review. Read the design contract before changing geometry.

## Select a real tool path

- Determine the target application and version. Distinguish neutral geometry delivery from native parametric modeling.
- Check which CAD kernel or application is actually available in the current environment before using it. The default system Python in this project currently lacks CadQuery and ezdxf; do not assume the project's CAD dependencies are installed.
- Smoke-test the selected CAD path with a simple known part and a real export/re-import.
- If the user's target is not accessible, provide a compatible exchange file or a clearly labeled script/macro and instructions. Do not claim native parametric history from a STEP file.

## Geometry and coordinate rules

- Use millimetres unless the contract states otherwise. Declare the origin and axes in the handoff.
- For robot models in this project, use global Z vertical, X chassis length, and Y chassis width.
- Build from the contract's master dimensions and interface register. Do not silently change agreed interfaces.
- Keep real geometry, simplified purchased-part envelopes, and illustrative geometry distinguishable in names and metadata.
- A CAD solid is not evidence of strength, stability, safe operation, or manufacturability.

## Autodesk Fusion native handoff

- When Fusion is the target, prefer a native `.f3d` design archive when the model can be created or exported through Fusion itself. Fusion assembly archives use `.f3z` where appropriate.
- Fusion's archive export API must run inside Fusion. Do not claim that a Replit-side CAD library or a renamed STEP file creates a native Fusion design.
- If Fusion is unavailable, provide a verified STEP exchange file and, when useful, a Fusion API script or clear import steps for the user to run in Fusion.
- Saving an imported STEP file as `.f3d` does not reconstruct the source model's original parametric feature history. State this limitation.

### Conversational Fusion model generation pilot

- The first system implementation is conversational and Skill-driven; do not add a user-facing UI before repeated design tasks prove it useful.
- For supported simple solids, prepare a version-1 JSON model specification using `Project_files_being_worked_on/fusion_native_pilot/README.md` and validate it with `fusion_model_spec.py`. The current schema supports millimetre, right-handed Z-up boxes and cylinders only.
- Run `generate_fusion_model.py` inside Autodesk Fusion to create native sketches, driving dimensions, user parameters, extrusion features, and an `.f3d` archive. The Replit environment cannot run the Fusion API.
- For external CAD geometry that cannot be recreated with the supported native features, use `convert_step_to_fusion_archive.py` inside Fusion. Label the result as imported B-rep geometry without recovered feature history.
- Review the generated report and the actual Fusion design. A local schema or syntax check does not count as a Fusion execution or engineering validation.

## STEP handoff

- STEP is the default neutral format for 3D parts and assemblies.
- For robot CAD handoffs, use native Fusion archives when Fusion is the target and they can be generated and checked; use STEP when requested or needed for neutral exchange.
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

