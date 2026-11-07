---
name: CAD export runtime
description: Environment constraint encountered while creating CadQuery STEP and mesh outputs.
---

CadQuery installed through the Python package manager, but its OpenCascade binding initially could not load because the system expat library was absent. Adding the Nix expat package enabled CadQuery and STEP round-trip checks; Python's bundled XML parser then showed an expat symbol mismatch, so XML-based 3MF validation was not reliable in that runtime.

**Why:** The CAD package combines native OpenCascade libraries with the workspace's wrapped Python runtime, and those system-library versions may not match.

**How to apply:** When regenerating CAD outputs, use the existing source and validate STEP with CadQuery re-import. Check 3MF ZIP integrity separately. Avoid changing `.replit` package configuration for one-off exports unless persistent regeneration is needed.
