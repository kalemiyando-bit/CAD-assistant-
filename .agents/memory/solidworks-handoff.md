---
name: CAD handoff targets
description: The user's planned primary CAD tool and neutral/native handoff preferences.
---

The user wants to transition fully from SolidWorks to Autodesk Fusion as their primary CAD tool. They are new to Fusion but have SolidWorks experience; explain Fusion workflows with concise SolidWorks comparisons when useful. Continue confirming the target software for each task because the system still supports other tools.
For Fusion-targeted work, prefer native `.f3d` design archives and `.f3z` assembly archives when they can be created or exported through Fusion. STEP remains a neutral exchange format; importing STEP and saving it as `.f3d` does not recreate the original parametric feature history.
For robot geometry, use millimetres and global Z vertical, X chassis length, and Y chassis width. These are model coordinates, not camera orientation.

**Why:** The user wants to move their own work from SolidWorks to Fusion, while the assistant system remains useful across other CAD tools.

**How to apply:** When teaching Fusion, do not assume prior Fusion familiarity; relate relevant concepts to SolidWorks without over-explaining general CAD. Ask for the target software and version for each design. If Fusion is selected, use native Fusion archives only when Fusion or its API can actually create and verify them; otherwise provide STEP and explain the feature-history limitation.
