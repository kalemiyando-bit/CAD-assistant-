# Parametric CAD source method

`build_gear_wheel_shaft.py` defines the demo dimensions in editable constants and generates the STEP, STL, 3MF, and DXF folders. The SolidWorks macro is a separate route that creates native feature-based parts when run inside SolidWorks.

## Dependencies

The script uses CadQuery for 3D solids/exports and ezdxf for 2D references. The tested versions are listed in `requirements.txt`.

## Regenerate

From the project root, install the listed Python dependencies and run:

```text
python attached_assets/robot_gear_wheel_shaft/05_parametric_source/build_gear_wheel_shaft.py
```

The script writes output to the sibling STEP, mesh, and DXF method folders. Change the constants near the start of the script to explore different demo dimensions.

This source is for a geometry-format test, not a validated drivetrain design. Its sampled gear flanks and simple shaft/wheel interfaces must not be used as manufacturing specifications.
