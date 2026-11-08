# Wheel Drive Bench Demonstrator — Design Contract

**Revision:** A0 — preliminary concept; Gate A is still open
**Status:** An exploratory envelope model specification has been prepared. No dimensions, interfaces, component, geometry, PCB, or firmware is approved for manufacture, assembly, or powered use.

## Purpose and operating context

- **Intended function:** A small, direct-drive wheel assembly for demonstrating forward/reverse motor control on a bench.
- **User-described assembly:** Car-style wheel/rim, shaft supported by a bearing, shaft coupled to a DC motor, and no external gears.
- **Control intent:** Car-like accelerator, brake, and handbrake behavior, with a separate stop control allowed. Exact controls and gesture mapping remain unresolved.
- **Operating environment:** Bench demonstration only. No vehicle, passenger, or specified payload use.
- **Target software:** Autodesk Fusion on Windows; exact version unknown. User is willing to learn to run a Fusion script if needed.
- **Agent-accessible tools:** Replit cannot run the Autodesk Fusion API. Native Fusion model creation must be run and inspected in the user's Fusion installation.
- **Research scope:** User sources only. No additional external research was performed for this concept.

## User requirements

| ID | Requirement | Source | Status/type | Verification |
|---|---|---|---|---|
| R-01 | Build one simple wheel-drive assembly with a wheel/rim, shaft, bearing support, and motor coupling. | User conversation | User-provided; interfaces open | Review model against approved assembly contract |
| R-02 | Use a small brushed DC motor; no external gear reduction. | User conversation | User-provided; exact motor open | Confirm selected motor and inspect assembly |
| R-03 | Provide a simple 2D drawing for each designed mechanical part. | User conversation | User-provided | Check drawing set against final model revision |
| R-04 | Provide a PCB and code for forward/reverse and car-like controls. | User conversation | User-provided; control mapping open | Schematic/PCB checks and firmware behavior review |
| R-05 | Prefer native Fusion formats where they can be created and checked; otherwise use compatible exchange formats. | User conversation | User-provided | Open/re-import files in the target application |

## Preliminary component research

These are candidates for discussion, not approved or user-supplied components:

- **Motor candidate:** Mabuchi FF-130SH-14230. Manufacturer data lists 6 V nominal voltage, 2.5–10 V operating range, 7,400 rpm no-load speed, 0.23 A at maximum efficiency, 1.20 mN·m maximum-efficiency torque, 6.67 mN·m stall torque, 1.03 A stall current, approximate dimensions 20.4 × 15.4 × 25.1 mm, and approximate mass 24 g. This is a high-speed, low-torque motor; suitability is limited to a guarded, unloaded or very lightly loaded bench demonstration unless later calculations show otherwise.
- **Motor-driver candidate:** TI DRV8833. Its datasheet lists a 2.7–10.8 V motor supply range and package-dependent current ratings. PWP/RTY packages are listed at 1.5 A RMS and 2 A peak per bridge under stated conditions; the PW package is listed at 500 mA RMS and 2 A peak. The datasheet provides forward, reverse, coast, and electrical-brake input states. Package thermal design, current limit, and the selected motor's actual behavior still require review.
- **Research sources:** [Mabuchi FF-130SH-14230 specifications](https://product.mabuchi-motor.com/detail.html?id=25); [Mabuchi product dimensions and performance table](https://product.mabuchi-motor.com/result.html); [TI DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf).

An electrical brake through an H-bridge is not a mechanical parking brake and does not establish that a loaded wheel will remain held.

## Deliverables and format plan

| Deliverable | Preferred format | Fallback / limitation |
|---|---|---|
| Parametric 3D assembly and parts | Fusion `.f3d`/`.f3z` created by Fusion | STEP only if it can be generated and checked; imported STEP does not restore feature history |
| Individual dimensioned drawings | Fusion drawing if a reliable Fusion workflow is established | Editable DXF and readable PDF |
| PCB and schematic | Editable Fusion Electronics project if a reliable workflow is established | Do not promise a native board file until Fusion Electronics can open and validate it |
| Firmware | Source code plus pin map and upload instructions | Exact controller board remains to be selected |

The Fusion pilot now supports boxes, cylinders, annular cylinders, centered-bore plates, and axis-aligned component placement. The updated path has not yet been executed in the user's Fusion. The concept specification uses assumed envelope dimensions and does not define joints, fits, retention, loads, or a verified motor coupling.

Autodesk's current documentation lists Fusion Electronics native files as `.fsch`, `.fbrd`, and `.flbr`, and EAGLE-compatible files as `.sch`, `.brd`, and `.lbr`. The Fusion Electronics API is currently preview/read-only for design changes; it can inspect designs and export EAGLE 9.6.2-compatible files, but it cannot create or edit board content through that public API. Therefore, native PCB creation must be performed in the Fusion Electronics UI unless a compatible import route is verified. The 2D drawing creation path also remains unverified.

## Open questions before architecture approval

| ID | Open item | Why it matters | Status |
|---|---|---|---|
| O-01 | Are the controls physical pedals/switches, button gestures, or both? | Determines PCB inputs and firmware | Button gestures stated; exact physical inputs unresolved |
| O-02 | What does one tap, double tap, hold, brake, handbrake, and stop each do? | Determines safe control state machine | Partially described; exact mapping unresolved |
| O-03 | Is the Mabuchi motor candidate acceptable and obtainable, or should another small motor be selected? | Determines shaft mount, motor driver, speed, and torque | Candidate only |
| O-04 | Wheel dimensions, shaft diameter, bearing size/spacing, and coupling dimensions | Required to model interfaces without inventing fits | Not user-specified; concept placeholders only |
| O-05 | Motor supply and controller power source | Required for component ratings and PCB power design | Not specified |
| O-06 | Exact Fusion version and whether the user can run the supplied script | Required to create and validate native Fusion files | Fusion on Windows; version unknown; user is willing to learn |
| O-07 | Drawing output format | Required to prepare editable/readable part drawings | DXF selected for the first editable import test; final per-part and native Fusion drawing formats remain open |
| O-08 | EDA software and version | Required to prepare an editable PCB project | Not specified |

## Verification and safety boundary

- Run the local Fusion model-spec tests before preparing a model specification.
- A Fusion-native archive can only be claimed after the script is run in Fusion and the resulting design is opened and inspected there.
- Do not treat a successful schema check or script generation as proof of native-file validity, fit, electrical safety, or motor performance.
- Keep the first physical test on a guarded bench with a current-limited supply. No vehicle-use, load capacity, parking-hold, or manufacturing-readiness claim is authorized.
- Record unavailable checks as blocked or not run; keep all selected values, calculations, assumptions, and sourced facts distinct.
