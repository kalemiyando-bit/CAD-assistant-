WHEEL DRIVE BENCH DEMONSTRATOR — WHEEL RIM POC-03
3D-ONLY FUSION HANDOFF

This folder contains one preliminary wheel-rim model specification. It does not
contain an assembly, a 2D drawing, or a duplicate of the Fusion add-in.

PRELIMINARY GEOMETRY

- Plain annular cylinder: 80 mm outside diameter × 6 mm nominal bore × 24 mm
  axial width.
- Axis: global +Y in a right-handed Z-up part coordinate system.
- Datum: center of the base annular face at the part origin; the part extends
  from Y=0 to Y=24 mm.
- These are assumed envelope values carried forward from the parent concept.
  The bore is not a specified fit. No hub, tread, spokes, fasteners, material,
  retention, load rating, or manufacturing process is defined.

CREATE THE NATIVE FUSION MODEL WITH THE EXISTING ADD-IN

1. In Autodesk Fusion on Windows, open Tools → Scripts and Add-Ins.
2. Select the existing `generate_fusion_model` script (version 1.1.0) and click
   Run. Do not add or install a duplicate copy.
3. Select `wheel_rim_POC03_model_spec.json` from this folder and choose an
   output folder.
4. Fusion should create a native `.f3d` archive and an adjacent report JSON.
5. Inspect the model in Fusion: millimetres, one component, 80 mm OD, 6 mm
   nominal bore, 24 mm width, +Y axis, base face centered at the origin, and an
   editable sketch/extrusion.
6. Reopen the `.f3d` archive in Fusion before recording the archive-open check
   as passed.

The annular-cylinder +Y path has not yet been verified in the user's Fusion
installation. Autodesk Fusion is not available in this Replit environment, so
this handoff cannot include the generated archive or claim that the native file
was created, inspected, or reopened. A valid specification is not proof of fit,
strength, safe speed, retention, or manufacturability.

Keep this part separate from the earlier shaft model. The project direction is
to review individual parts before making an assembly. The next likely
component is the hub, but its geometry and interface must remain a separate
part-level decision.
