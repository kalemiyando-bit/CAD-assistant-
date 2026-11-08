WHEEL-SIDE SHAFT — POC-02 FUSION HANDOFF

This is a 3D-only folder. It contains no 2D drawing, DXF, ZIP, or duplicate
Fusion add-in.

MODEL

- One preliminary cylinder: Ø6 mm × 46 mm.
- The shaft axis is global +Y in a right-handed, Z-up model.
- The cylinder base center is at the origin.
- Values reuse the old A0 workflow envelope; they are not approved dimensions,
  fits, strength values, or manufacturing instructions.

CREATE THE NATIVE FUSION MODEL WITH YOUR EXISTING ADD-IN

1. In Fusion, open Tools → Scripts and Add-Ins and select your existing
   generate_fusion_model script (version 1.1.0).
2. Click its Run button; do not choose “Add Script from device” again.
3. When prompted, select wheel_drive_shaft_POC02_model_spec.json from this
   folder and choose an output folder.
4. Fusion should create a native .f3d archive and an adjacent report JSON.
5. Inspect the design in Fusion: millimetres, one component, Ø6 mm diameter,
   46 mm length, +Y axis, base at the origin, and editable sketch/extrusion.
   Reopen the archive before treating the archive-open check as passed.

The add-in bundle is intentionally omitted because the user already has the
tested script installed. Its shared source remains in
Project_files_being_worked_on/fusion_native_pilot if a clean installation is
ever needed. Fusion itself is not available in this Replit environment. Local
model-spec validation does not prove the generated .f3d opens correctly or that
the part fits, is strong, safe, or manufacturable. The +Y generator path still
needs inspection in the user's Fusion version.

For the full brief and limits, see wheel_drive_shaft_POC02_brief.txt.
