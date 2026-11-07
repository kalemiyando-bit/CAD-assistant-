---
name: CAD handoff targets
description: The user's planned primary CAD tool and neutral/native handoff preferences.
---

Autodesk Fusion is the user's planned primary CAD target. Continue asking which software is intended for each design task because the system must still support other tools.
For Fusion-targeted work, prefer native `.f3d` design archives and `.f3z` assembly archives when they can be created or exported through Fusion. STEP remains a neutral exchange format; importing STEP and saving it as `.f3d` does not recreate the original parametric feature history.
For robot geometry, use millimetres and global Z vertical, X chassis length, and Y chassis width. These are model coordinates, not camera orientation.

**Why:** The user is planning to change the system's primary CAD software to Autodesk Fusion while retaining support for other CAD tools.

**How to apply:** Ask for the target software and version for every design. If Fusion is selected, use native Fusion archives only when Fusion or its API can actually create and verify them; otherwise provide STEP and explain the feature-history limitation.
