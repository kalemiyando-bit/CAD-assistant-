---
name: CAD export runtime
description: Environment constraint encountered while creating CadQuery STEP and mesh outputs.
---

The CAD generator declares CadQuery and ezdxf in the project Python dependencies, but bare system `python` did not import either during a later check. Do not assume the shell's default interpreter is the project's CAD environment. CadQuery's OpenCascade binding has also required a compatible system expat library; Python's bundled XML parser showed an expat symbol mismatch in an earlier runtime, so XML-based 3MF validation was unreliable there.

**Why:** CAD dependencies and native OpenCascade libraries may be available only in the selected project environment, and system-library versions may not match the wrapped Python runtime.

**How to apply:** Before generating CAD, verify which Python environment is active and whether CadQuery/ezdxf import there; use the existing project dependency setup or package-management guidance rather than assuming bare `python` is correct. Validate STEP with CadQuery re-import. Check 3MF ZIP integrity separately. Avoid changing `.replit` package configuration for one-off exports unless persistent regeneration is needed.
