WHEEL-SIDE SHAFT — POC-02 FUSION HANDOFF

This is a 3D-only package. It contains no 2D drawing or DXF deliverable.

MODEL

- One preliminary cylinder: Ø6 mm × 46 mm.
- The shaft axis is global +Y in a right-handed, Z-up model.
- The cylinder base center is at the origin.
- Values reuse the old A0 workflow envelope; they are not approved dimensions,
  fits, strength values, or manufacturing instructions.

CREATE THE NATIVE FUSION MODEL

1. Extract wheel_drive_shaft_POC02_Fusion_bundle.zip and preserve its folders.
2. In Fusion, open Tools → Scripts and Add-Ins → Add Script from device.
3. Select the extracted fusion_native_pilot/generate_fusion_model folder.
4. Run “Generate Fusion Model from JSON.”
5. Select wheel_drive_shaft_POC02_model_spec.json from the extracted package and
   choose an output folder.
6. Fusion should create a native .f3d archive and an adjacent report JSON.
7. Inspect the design in Fusion: millimetres, one component, Ø6 mm diameter,
   46 mm length, +Y axis, base at the origin, and editable sketch/extrusion.
   Reopen the archive before treating the archive-open check as passed.

Fusion itself is not available in this Replit environment. The local model-spec
validation does not prove the generated .f3d opens correctly or that the part
fits, is strong, safe, or manufacturable. The +Y generator path still needs
inspection in the user's Fusion version.

For the full brief and limits, see wheel_drive_shaft_POC02_brief.txt.
