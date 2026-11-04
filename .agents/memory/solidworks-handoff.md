---
name: SolidWorks handoff
description: The user's preferred CAD workflow for the robot design.
---

The user plans to continue designing the robot in SolidWorks and wants CAD geometry that can be imported and edited there.
For robot CAD deliverables, provide STEP files only; do not include other exported file formats.
The robot's main coordinate frame must use global Z for vertical, X for chassis length, and Y for chassis width. The user means the model coordinate frame, not the camera view, when asking for Z-up.

**Why:** The user stated they intend to import generated files into their SolidWorks software and continue modifying them.

**How to apply:** Export separate part STEP files and coordinated assembly STEP files only. Keep the robot's actual model coordinates Z-up; don't treat a camera rotation as changing the main axes. Model dimensions in millimetres, and explain that STEP does not preserve a native SolidWorks feature tree.
