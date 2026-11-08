# Preliminary Concept Review — A0

- **Design / revision:** Wheel Drive Bench Demonstrator / A0
- **Contract:** `DESIGN_CONTRACT.md` / A0 draft
- **Reviewer:** Coordinating agent
- **Independence:** Non-independent review by the creator; no separate reviewer was available
- **Files reviewed:** `preliminary_wheel_drive_spec.json`, `PRELIMINARY_CONCEPT.md`, `DESIGN_CONTRACT.md`, and the Fusion model-spec/generator source
- **Target software/version:** Autodesk Fusion on Windows; exact version unknown

## Findings

| ID | Severity | Requirement/interface | Finding | Evidence | Required action |
|---|---|---|---|---|---|
| F-01 | Blocker | R-01, R-03; wheel/shaft/bearing/coupling interfaces | Every mechanical size in the concept is provisional; no fit, tolerance, retention, load, or material is approved. | The concept JSON labels assumptions; no measured components or approved dimensions were supplied. | Confirm real component dimensions and interfaces before detailing or manufacture. |
| F-02 | Blocker | R-02; powered bench operation | The existing motor candidate's listed 7,400 rpm no-load speed implies about 31 m/s rim speed with an 80 mm wheel (`π × 0.08 × 7400 / 60`). This is a calculation, not a measured operating speed. | Candidate data and source links in `DESIGN_CONTRACT.md`; calculation repeated in `PRELIMINARY_CONCEPT.md`. | Do not power the concept until a speed limit, guard, and test procedure are defined and checked. |
| F-03 | Major | R-04; control behavior and electronics | No PCB or firmware is included. The button description does not fully map tap, double-tap, hold, forward/reverse, braking, handbrake, and stop; motor, controller, supply, and EDA tool are also unresolved. | Open items O-01, O-02, O-03, O-05, and O-08 in the contract. | Agree on the control state table and hardware interfaces before electrical design. |
| F-04 | Major | R-05; Fusion-native output | The Fusion API generator was not run in Autodesk Fusion. No `.f3d` archive or second-session reopen evidence exists. | Replit does not have Autodesk Fusion; local checks cover the JSON and Python syntax only. | Run the packaged script in the user's Fusion installation and inspect the result. |
| F-05 | Major | R-03; individual 2D drawings | No drawing files are included because the requested drawing format has not been confirmed. | The concept is only a model specification and handoff note. | Confirm DXF, Fusion drawing, PDF, or a combination before drafting. |

## Checks

| Check | Result | Evidence | Limitation |
|---|---|---|---|
| Requirements traceability | PASS | Contract and model assumptions are explicit and linked to the concept specification. | User approval of the assumed dimensions is still missing. |
| Model-spec validation | PASS | 18 standard-library tests pass, including the seven-component concept specification. | Schema validation does not create or validate CAD geometry. |
| Geometry/dimensions/interfaces | BLOCKED | Expected principal extents are calculated for the specified axis orientations. | Fusion execution, bore inspection, mating fit, strength, and interference checks are not run. |
| Target-software import/readability | BLOCKED | Same-named script folders, entry points, manifests, and helper loading are packaged. | The script and generated archive have not been opened in Fusion. |
| PCB/electrical checks | NOT RUN | None. | No board or firmware exists; critical electrical inputs remain unknown. |
| Release files and manifest | PASS | `PRELIMINARY-MANIFEST.json` records hashes for this concept package. | Package integrity is not design validation or release approval. |

## Overall status

- **Status:** BLOCKED for manufacture and powered testing; suitable only as a preliminary concept package for review.
- **Unresolved assumptions or safety concerns:** Provisional dimensions, unverified coupling and motor interfaces, high candidate rim speed, and undefined electrical/control behavior.
- **Required changes and re-checks:** Replace assumptions with confirmed interfaces, define guarded speed limits and controls, select components/EDA software, prepare the requested drawings, then run and inspect the Fusion output.
