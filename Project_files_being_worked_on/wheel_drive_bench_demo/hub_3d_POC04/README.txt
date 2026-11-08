WHEEL DRIVE BENCH DEMONSTRATOR — HUB POC-04
3D-ONLY PART SPECIFICATION

This folder contains one preliminary hub model specification. It does not
contain an assembly, a 2D drawing, or a duplicate of the Fusion add-in.

PRELIMINARY GEOMETRY

- Plain annular cylinder: 30 mm outside diameter × 6 mm nominal bore × 8 mm
  axial width.
- Axis: global +Y in a right-handed Z-up part coordinate system.
- Datum: center of the base annular face at the part origin; the part extends
  from Y=0 to Y=8 mm.
- These values are assumptions carried forward from the parent A0 concept. The
  bore does not define a fit. No flange, fasteners, keyway, retention, material,
  or manufacturing process is specified.

VERIFICATION TIMING

Per the user's direction, verify the planned parts together after all of them
have been created. Do not treat this JSON as a checked Fusion model.

When the part set is ready for that verification pass:

1. In Autodesk Fusion on Windows, open Tools → Scripts and Add-Ins.
2. Select the existing `generate_fusion_model` script (version 1.2.0) and click
   Run; do not add or install a duplicate copy.
3. Select `hub_POC04_model_spec.json` and choose an output folder.
4. Inspect one component, millimetres, 30 mm OD, 6 mm nominal bore, 8 mm width,
   +Y axis, base face centered at the origin, and the editable sketch/extrusion.
5. Reopen the resulting `.f3d` archive before recording the archive-open check
   as passed.

Fusion is not available in this Replit environment. The generated native model,
fit, retention, strength, safety, and manufacturability remain unverified.
