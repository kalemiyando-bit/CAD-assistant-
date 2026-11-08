# Wheel Drive Bench Demonstrator — Design Contract

**Revision:** A0 / POC-02 3D-only handoff — preliminary concept; full-system Gate A is still open
**Status:** An exploratory envelope model specification has been prepared. No dimensions, interfaces, component, geometry, PCB, or firmware is approved for manufacture, assembly, or powered use.

## Purpose and operating context

- **Intended function:** A simple, bench-only, direct-drive wheel module for demonstrating speed increase, decrease, and measurement with a small brushed DC motor; not a vehicle.
- **User-described assembly:** Wheel and hub on a wheel-side shaft supported by a bearing/support, coupled to a motor-side shaft and motor. No external gear reduction. The motor's integrated shaft may serve as the motor-side shaft.
- **Control intent:** GAS and BRAKE buttons; one tap changes the speed target by one level, while holding gradually raises or lowers the target. BRAKE can reduce the target to zero. Include a separate handbrake/emergency-stop control and wheel-speed measurement. No reverse.
- **Operating environment:** Bench demonstration only. No vehicle, passenger, or specified payload use.
- **Target software:** Autodesk Fusion on Windows; exact version unknown. User is willing to learn to run a Fusion script if needed.
- **Agent-accessible tools:** Replit cannot run the Autodesk Fusion API. Native Fusion model creation must be run and inspected in the user's Fusion installation.
- **Research scope:** User sources only. No additional external research was performed for this concept.

## User requirements

| ID | Requirement | Source | Status/type | Verification |
|---|---|---|---|---|
| R-01 | Develop a simple bench-only wheel-drive proof of concept, one part at a time; create the assembly after the individual parts are reviewed. | User conversation | User-provided | Review each part, then the assembled interfaces |
| R-02 | Use a small brushed DC motor with no external gear reduction. | User conversation | User-provided; exact motor and interfaces open | Confirm the selected motor and inspect the assembly |
| R-03 | Provide 3D Fusion handoffs for individual mechanical parts, one at a time; defer 2D drawings and profiles unless requested. | User conversation, 2026-11-08 | User-provided current scope | Open and inspect each generated 3D part in Fusion |
| R-04 | Use GAS and BRAKE buttons: taps change one speed level, holds ramp speed up or down; braking can reach zero. Include a separate handbrake/emergency stop. | User conversation | User-provided behavior; implementation and stop dynamics unresolved | Review the control state machine and test with selected hardware |
| R-05 | Measure wheel speed; do not implement reverse. | User conversation | User-provided | Confirm speed feedback and verify reverse is absent |
| R-06 | Use simple, sensible preliminary dimensions where specifications are absent, and label them as assumptions for this proof of concept. | User conversation | User-authorized preliminary design discretion; no dimensions approved | Review and replace assumptions as components are selected |
| R-07 | Provide a PCB and code for the simple speed-control behavior after mechanical/electrical requirements are established. | User conversation | User-provided long-term goal; deferred | Schematic/PCB checks and firmware behavior review |
| R-08 | Prefer native Fusion formats where they can be created and checked; otherwise use compatible exchange formats. | User conversation | User-provided | Open/re-import files in the target application |

## Current preliminary control targets (unvalidated)

The user authorized sensible preliminary choices but has not supplied motor or
controller specifications. The following are assumptions, not confirmed
performance or safety ratings:

- Maximum commanded wheel speed: 300 rpm.
- One tap changes the target by 25 rpm (12 increments from zero to the cap).
- Holding a button ramps the target at 30 rpm/s, upward for GAS and downward for
  BRAKE, with BRAKE reaching zero.
- Measure and display wheel rpm.
- Treat the handbrake/emergency-stop input as a latched drive-disable request
  until the selected controller's stopping behavior is reviewed.
- At the placeholder 80 mm wheel diameter, 300 rpm is approximately 1.26 m/s
  rim speed (calculated, not measured). This is not a safe operating limit.

The earlier POC-01 DXF is retained as a prior handoff, not an active deliverable.
The current 3D-only shaft handoff is recorded in
`shaft_3d_POC02/wheel_drive_shaft_POC02_brief.txt`.

## Preliminary component research

These are candidates for discussion, not approved or user-supplied components:

- **Motor candidate:** Mabuchi FF-130SH-14230. Manufacturer data lists 6 V nominal voltage, 2.5–10 V operating range, 7,400 rpm no-load speed, 0.23 A at maximum efficiency, 1.20 mN·m maximum-efficiency torque, 6.67 mN·m stall torque, 1.03 A stall current, approximate dimensions 20.4 × 15.4 × 25.1 mm, and approximate mass 24 g. This is a high-speed, low-torque motor; suitability is limited to a guarded, unloaded or very lightly loaded bench demonstration unless later calculations show otherwise.
- **Motor-driver candidate:** TI DRV8833. Its datasheet lists a 2.7–10.8 V motor supply range and package-dependent current ratings. PWP/RTY packages are listed at 1.5 A RMS and 2 A peak per bridge under stated conditions; the PW package is listed at 500 mA RMS and 2 A peak. The datasheet provides forward, reverse, coast, and electrical-brake input states. Package thermal design, current limit, and the selected motor's actual behavior still require review.
- **Research sources:** [Mabuchi FF-130SH-14230 specifications](https://product.mabuchi-motor.com/detail.html?id=25); [Mabuchi product dimensions and performance table](https://product.mabuchi-motor.com/result.html); [TI DRV8833 datasheet](https://www.ti.com/lit/ds/symlink/drv8833.pdf).

An electrical brake through an H-bridge is not a mechanical parking brake and does not establish that a loaded wheel will remain held.

## Deliverables and format plan

| Deliverable | Preferred format | Fallback / limitation |
|---|---|---|
| Individual 3D parts and final assembly | Native Fusion `.f3d`/`.f3z` created by Fusion | STEP only if requested and verified; imported STEP does not restore feature history |
| 2D drawings or profiles | Not requested for the current phase | Revisit only if the user asks |
| PCB and schematic | Editable Fusion Electronics project if a reliable workflow is established | Do not promise a native board file until Fusion Electronics can open and validate it |
| Firmware | Source code plus pin map and upload instructions | Exact controller board remains to be selected |

The Fusion pilot supports boxes, cylinders, annular cylinders, centered-bore plates, and axis-aligned component placement. The user now reports that the single-part shaft example passed and can produce a 3D model; this does not confirm that every supported feature or the full wheel-drive design has been tested in Fusion. The exact Fusion-side checks for the shaft still need to be recorded. The concept specification uses assumed envelope dimensions and does not define joints, fits, retention, loads, or a verified motor coupling.

Autodesk's current documentation lists Fusion Electronics native files as `.fsch`, `.fbrd`, and `.flbr`, and EAGLE-compatible files as `.sch`, `.brd`, and `.lbr`. The Fusion Electronics API is currently preview/read-only for design changes; it can inspect designs and export EAGLE 9.6.2-compatible files, but it cannot create or edit board content through that public API. Therefore, native PCB creation must be performed in the Fusion Electronics UI unless a compatible import route is verified. The 2D drawing creation path also remains unverified.

## Open questions before architecture approval

| ID | Open item | Why it matters | Status |
|---|---|---|---|
| O-01 | Which physical button, sensor, display, and controller parts will be used? | Determines interfaces and electrical behavior | GAS/BRAKE and a separate handbrake/emergency input are requested; hardware is unselected |
| O-02 | What latching and braking/coasting behavior does the emergency control require? | Determines safe control state machine and stop response | Drive-disable request is proposed; actual stopping behavior remains unresolved |
| O-03 | Is the Mabuchi motor candidate acceptable and obtainable, or should another small motor be selected? | Determines shaft mount, motor driver, speed, and torque | Candidate only |
| O-04 | Wheel dimensions, shaft interfaces, bearing size/spacing, and coupling dimensions | Required to model interfaces and fit | User authorized sensible POC assumptions; current A0 values remain placeholders |
| O-05 | Motor supply and controller power source | Required for component ratings and PCB power design | Not specified |
| O-06 | Exact Fusion version and whether the user can run the supplied script | Required to create and validate native Fusion files | Fusion on Windows; version unknown; user is willing to learn |
| O-07 | 2D drawing output format | Needed only if the user later requests 2D work | No 2D outputs requested for the current phase |
| O-08 | EDA software and version | Required to prepare an editable PCB project | Not specified |

## Verification and safety boundary

- Run the local Fusion model-spec tests before preparing a model specification.
- A Fusion-native archive can only be claimed after the script is run in Fusion and the resulting design is opened and inspected there.
- Do not treat a successful schema check or script generation as proof of native-file validity, fit, electrical safety, or motor performance.
- Do not recommend powered testing until a physical wheel guard, a current-limited test procedure, a speed limit, and verified stop behavior are defined for the selected hardware.
- Keep any later test on a guarded bench with a current-limited supply. No vehicle-use, load capacity, parking-hold, or manufacturing-readiness claim is authorized.
- Record unavailable checks as blocked or not run; keep all selected values, calculations, assumptions, and sourced facts distinct.
