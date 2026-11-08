---
name: Fusion script folder layout
description: The folder structure Autodesk Fusion expects when adding a local script from device.
---

For Fusion's "Script or add-in from device" action, the selected folder must contain a script and `.manifest` file with matching base names, and the folder name must match that base name. Keep dependent local modules alongside the script.

**Why:** Fusion rejected the `fusion_native_pilot` parent folder because the script and manifest are named `generate_fusion_model`, not `fusion_native_pilot`.

**How to apply:** Package the generator in a `generate_fusion_model` folder with `generate_fusion_model.py`, `generate_fusion_model.manifest`, and its imported validator module. Select that child folder in Fusion.

The user wants one standard `generate_fusion_model` add-in for all designs made by this system, with single-file and multi-file JSON selection; do not create a new add-in for each part.

**Why:** The user wants to use the existing tested add-in and avoid repeating Fusion add-in setup for every design.

**How to apply:** Extend the existing package in place. When several model-spec JSON files are selected, create one separate Fusion design/archive/report per specification; a single specification with multiple components remains one design.
