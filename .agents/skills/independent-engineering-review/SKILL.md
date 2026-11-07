---
name: independent-engineering-review
description: Independently checks an engineering design, CAD package, drawing, PCB, simulation, or agent handoff against its contract. Use before release or when asked to review engineering output.
---

# Independent Engineering Review

Review the design contract and actual source/deliverables. Do not edit the designer's files. Return findings and change requests to the coordinator.

## Independence

- Prefer a reviewer agent that was not the author and has the contract plus deliverables.
- Check the actual files and source data; do not accept the creator's report as proof.
- Recompute critical reported numbers from source data or a small script where practical.
- If no separate reviewer is available, label the result “non-independent review”; do not claim independent validation.

## Check against evidence

- Trace important geometry, dimensions, electrical values, and claims to contract requirements.
- Inspect units, coordinates, interfaces, file structure, and target-software import/readability.
- Check for missing files, empty files, changed outputs, stale drawings, and inconsistencies between model and schedule.
- For simulations, check assumptions, convergence or sensitivity, conservation/balance, and the actual quantity of interest.
- For mechanical CAD, distinguish envelope geometry from detailed or validated parts.
- For 2D drawings and schematics, include human legibility and visual correctness, not just parsability or a zero-error counter.
- For PCB work, inspect warnings, netlist consistency, rules, and manufacturer-specific constraints.
- Identify unresolved supplier data, safety factors, physical tests, or expert reviews.

## Report

Use `../engineering-design-coordinator/references/review-report.md`. Every finding must include evidence and affected requirement/interface. Mark checks PASS, FAIL, BLOCKED, or NOT RUN. Missing evidence is not a pass.

Return a change request using `../engineering-design-coordinator/references/change-request.md`; do not change the owned design. Never certify a design or claim that simulation proves physical performance.

