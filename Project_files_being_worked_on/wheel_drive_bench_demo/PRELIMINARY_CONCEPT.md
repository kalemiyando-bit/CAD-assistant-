# Wheel Drive Bench Demonstrator — Preliminary Concept A0

**Status:** Exploratory envelope only. Not approved for manufacture, assembly, or powered testing. Gate A remains open.

## User-provided intent

- A small, bench-only, direct-drive wheel module with a wheel/rim, shaft, bearing support, and motor coupling.
- A small brushed DC motor; no external gear reduction.
- Forward/reverse control with button gestures, a PCB, and firmware eventually.
- Autodesk Fusion on Windows is the target. The exact Fusion version is not known.
- Research is limited to sources already supplied or recorded in the project; no additional browsing was used for this concept.

## Concept geometry

The model uses a horizontal wheel axis along global **+Y**, with global **+Z** vertical and **+X** across the support. The source is `preliminary_wheel_drive_spec.json`.

| Component | Preliminary envelope (mm) | Status |
|---|---:|---|
| Wheel rim | 80 OD × 24 wide, 6 bore | Placeholder reused from a separate file-format test |
| Hub | 30 OD × 8 projection, 6 bore | Placeholder reused from a separate file-format test |
| Shaft | 6 diameter × 46 long | Unverified assumption |
| Bearing | 12 OD × 6 ID × 4 wide | Envelope assumption only; no bearing selected |
| Bearing support | 30 × 30 × 4 plate, centered 12 bore | Envelope assumption only |
| Coupling | 10 diameter × 10 long | Packaging envelope only; no bores or coupling selected |
| Motor body | 20.4 × 15.4 × 25.1 | Candidate FF-130 envelope from the existing contract; motor not selected |

The wheel/hub, shaft/bearing, support, coupling, and candidate motor are separate Fusion components. Coincident surfaces and overlaps represent conceptual interfaces, not verified fits or joint definitions. The wheel and coupling do not include tread, retention, fastening, motor-shaft, or key features.

## Evidence and assumptions

- The Mabuchi FF-130SH-14230 is only a candidate documented in the existing design contract, not a selected part. That contract records 6 V nominal, 7,400 rpm no-load, and body dimensions of about 20.4 × 15.4 × 25.1 mm, citing the Mabuchi product pages.
- At the candidate's listed 7,400 rpm no-load speed, an 80 mm wheel would have a calculated rim speed of about **31 m/s** (`π × 0.08 m × 7400 / 60`). This is a calculation from candidate data, not a measured result. Do not power this concept until a speed limit and physical guard are defined and checked.
- The existing contract lists the TI DRV8833 as a possible bridge, but its usable current depends on package and thermal conditions. It is not selected, and no PCB layout or firmware is included.
- The dimensions above are deliberately provisional. They are not user-approved interface dimensions and do not establish fit, strength, speed capability, retention, or manufacturability.

## Controls and electronics remain open

The recorded user intent is: tap/toggle to run in a direction at the current speed level; double-tap changes speed by one level; holding changes speed progressively. The exact mapping between each button/gesture, forward/reverse, acceleration/deceleration, braking, handbrake, and stop is not yet defined. No firmware or PCB should be treated as buildable until that mapping, controller, motor, supply, connectors, and electrical limits are agreed.

## Fusion handoff and verification

1. Copy `fusion_native_pilot/` and this folder to a location accessible to Fusion on Windows, keeping the nested script folders in place.
2. In Fusion, open **Tools → Scripts and Add-Ins**, choose **Add Script from device**, and select `fusion_native_pilot/generate_fusion_model/`.
3. Run **Generate Fusion Model from JSON**, select `preliminary_wheel_drive_spec.json`, then choose an output folder.
4. Inspect the component axes, bearing/support opening, shaft path, and candidate motor envelope in Fusion. Then reopen the exported `.f3d` archive in a separate Fusion session.

The Replit environment cannot run Autodesk Fusion. The Fusion script, `.f3d` export, second-session reopen, clearances, and fit have **not** been run or verified here. The generated design will remain a preliminary native CAD handoff, not an engineering release.

The checks completed so far are recorded in `REVIEW_A0.md`. That is a non-independent review by the creator, not an independent engineering approval. `PRELIMINARY-MANIFEST.json` checks package file integrity only.

## Next engineering inputs

- Confirm or replace the wheel, hub, shaft, bearing, support, and motor-coupling dimensions.
- Select the motor and verify its shaft dimensions, operating voltage, current, and loaded speed from its datasheet.
- Define a guarded maximum speed and bench-test procedure before powered operation.
- Resolve button gestures and define the motor driver, controller, supply, connectors, and stop behavior.
- Confirm the requested drawing format and the exact Fusion version before preparing release drawings.
