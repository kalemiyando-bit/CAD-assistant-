# Shaft 2D workflow test — A0

This is the first single-part drafting test for the Wheel Drive Bench
Demonstrator.

## Files

- `shaft_6x46_A0_R12_retry.dxf` — minimal R12 ASCII DXF import retry in
  millimetres, with all entities on the default layer.
- `shaft_6x46_A0_preview.html` — self-contained visual preview with a DXF download
  link.
- `generate_shaft_drawing.py` — regenerates both files from the shaft entry in
  `../preliminary_wheel_drive_spec.json`.

## Design status

The part is a plain cylindrical envelope, diameter 6 mm by length 46 mm, with
its axis along +Y. These are provisional values copied from the A0 concept
specification for testing the design workflow. They are not confirmed component
dimensions. End shape, material, tolerance, finish, and retention features are
not specified. This drawing is not for manufacture.

The first AC1015/AutoCAD 2000 DXF attempt (`shaft_6x46_A0.dxf`) failed to insert
in the user's Fusion 2026 installation. It is retained only for comparison. The
current download uses a simpler R12 ASCII structure, but still needs an actual
Fusion import test.

## Fusion import test

1. Open Fusion and start a new design.
2. Create a sketch on a plane.
3. Use **Insert DXF** and select `shaft_6x46_A0_R12_retry.dxf`; keep the import
   units in millimetres.
4. Finish the sketch and inspect the side view, end view, labels, and dimensions.

The DXF contains a full sheet layout. Imported dimensions and notes are ordinary
2D annotation geometry, not associative Fusion drawing dimensions. The R12
retry has not yet been tested in Fusion; report any error text or missing text
before using the same method for more parts.
