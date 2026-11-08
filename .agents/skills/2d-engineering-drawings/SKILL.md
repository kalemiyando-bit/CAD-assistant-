---
name: 2d-engineering-drawings
description: Produces or reviews dimensioned 2D engineering drawings and CAD layouts from a design contract or 3D model. Use for Autodesk Fusion, AutoCAD, SolidWorks drawings, DXF, PDF, and related drafting tasks.
---

# 2D Engineering Drawings

Follow the engineering-design coordinator Skill. Ask which drafting/CAD software and version the user is using unless already stated.

Before creating a 2D deliverable, ask what it is for:

- **Model-building sketch:** geometry the user will import into a sketch and use to create 3D features.
- **Documentation drawing:** a readable, dimensioned sheet for communicating or recording a design.
- **Both:** create separate deliverables for each purpose; do not reuse one DXF for both.

Confirm whether the user wants an editable native drawing, neutral 2D exchange file, print-ready sheet, or a combination. Explain that a DXF inserted into a Fusion sketch becomes sketch entities: borders, title blocks, dimension graphics, and text are geometry, not native drawing annotations or associative sketch dimensions.

## Source and dimensions

- Derive views and dimensions from the approved model or a verified dimension schedule.
- Do not infer exact dimensions from an unscaled sketch, photo, or AI-generated image.
- Keep drawings consistent with the model revision and interfaces. Label preliminary, calculated, supplier-dependent, and to-be-confirmed values.
- Avoid adding dimensions that conflict or overconstrain a drawing.

## Format selection

- STEP is 3D geometry, not a dimensioned 2D drawing sheet.
- Use the target application's native drawing format only when the application/tool is actually available or the native file can be reliably created.
- DXF is a practical editable 2D exchange format; PDF is a practical readable sheet format. Confirm the user's requested formats before exporting.
- Preserve units, scale, projection convention, revision, title, and material/process notes where applicable.
- For a **model-building sketch**, include only the closed profiles and any explicitly requested construction geometry needed for the intended 3D feature. Omit sheet borders, title blocks, dimension/extension/leader lines, dimension text, and documentation notes. Supply needed sizes and feature instructions separately; a DXF does not make its text into native Fusion dimensions.
- For **documentation**, include the views, dimensions, notes, and sheet details needed to communicate the part. Do not suggest inserting this full sheet into a modeling sketch unless the user deliberately wants all of that linework as sketch geometry. Prefer a readable PDF or a verified native drawing workflow for sheet documentation.
- If the purpose is unclear, ask before generating the file. If both purposes are requested, keep the modeling profile and documentation sheet as separate deliverables.

## Review

- Confirm each view corresponds to the same revision and coordinate frame.
- Check dimensions against the source model/schedule, units, scale, projection, line visibility, sheet fit, and text readability.
- Open or parse the exported file with an available tool where possible. A successful write command is not a readability check.
- Request a human visual review for ambiguous views, critical dimensions, and manufacturing intent.
- Do not claim a drawing is production-ready unless tolerances, fits, materials, and manufacturing requirements have been reviewed.

