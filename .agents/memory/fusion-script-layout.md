---
name: Fusion script folder layout
description: The folder structure Autodesk Fusion expects when adding a local script from device.
---

For Fusion's "Script or add-in from device" action, the selected folder must contain a script and `.manifest` file with matching base names, and the folder name must match that base name. Keep dependent local modules alongside the script.

**Why:** Fusion rejected the `fusion_native_pilot` parent folder because the script and manifest are named `generate_fusion_model`, not `fusion_native_pilot`.

**How to apply:** Package the generator in a `generate_fusion_model` folder with `generate_fusion_model.py`, `generate_fusion_model.manifest`, and its imported validator module. Select that child folder in Fusion.
