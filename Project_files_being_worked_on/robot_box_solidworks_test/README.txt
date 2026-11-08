SOLIDWORKS FORMAT TEST — RECTANGULAR BLOCK

Geometry: one solid cuboid, 100 x 60 x 40 mm. Origin at one corner; X=100, Y=60, Z=40. Units in STEP/3MF and DXF are millimetres.

FILES
- rectangular_block_100x60x40_AP214.step — primary solid B-rep exchange file.
- rectangular_block_100x60x40_AP214.stp — same STEP content with alternate extension.
- rectangular_block_100x60x40_binary.stl — triangulated mesh; useful for viewing/printing, not a feature-based CAD solid.
- rectangular_block_100x60x40.3mf — triangulated mesh package; not a feature-based CAD solid.
- rectangular_block_orthographic_mm.dxf — 2D top/front/side outlines and reference dimensions; suitable for sketch/drawing import.

STEP caveat: STEP carries exact solid geometry, but not an editable SolidWorks feature tree. The STEP file is hand-authored as an analytic planar B-rep and its entity references/topology were checked programmatically; it has not been opened in SolidWorks in this environment.

Not included: native .SLDPRT/.SLDASM, Parasolid .x_t/.x_b, or IGES. Those require a CAD exporter or SolidWorks itself; I will not fake those file extensions.
