# Gear, wheel, shaft, and assembly format comparison

This is a **format test package** for importing and editing three demo components in SolidWorks. Each method has its own folder and README.

## Method folders

1. `01_solidworks_native_macro/` — VBA macro source. Run it inside SolidWorks to create native editable `.SLDPRT` files and a `.SLDASM` assembly.
2. `02_step_exchange/` — separate STEP part files and a STEP assembly.
3. `03_mesh_formats/` — separate STL and 3MF meshes, plus combined assembly meshes. Meshes are for viewing/printing, not feature-based CAD editing.
4. `04_dxf_2d/` — 2D DXF profiles and layout references; these are not 3D models.
5. `05_parametric_source/` — CadQuery source and dependencies used to generate STEP, mesh, and DXF deliverables.

## Demo geometry

| Component | Demo dimensions |
|---|---|
| Spur gear | 18 teeth, module 2, 20° pressure angle, 15 mm face, 12 mm bore; nominal pitch diameter 36 mm, outside diameter 40 mm, root diameter 31 mm |
| Wheel | 80 mm outside diameter, 24 mm rim width, 30 mm hub, 8 mm hub projection, 12 mm bore |
| Shaft | 12 mm diameter × 100 mm long |
| Assembly | Gear begins at 10 mm and wheel begins at 55 mm along the shaft axis |

These values exist only to compare authoring and import methods. The gear tooth flanks are sampled straight-segment approximations, and the parts have no keyways, retention hardware, bearings, load rating, or engineering validation.

## Recommended SolidWorks test order

- For a native feature tree, run the macro and open its `.SLDPRT` and `.SLDASM` outputs.
- For neutral solid geometry, open `02_step_exchange/GearWheelShaftDemo_assembly.step`.
- Use STL/3MF only to compare mesh imports.
- Import DXF only when testing 2D sketch/reference workflows.

The STEP files were generated and checked with a CAD kernel, but they have not been opened in SolidWorks here. The macro source has not been run in SolidWorks. If an import or macro error appears, capture the full message and SolidWorks version.
