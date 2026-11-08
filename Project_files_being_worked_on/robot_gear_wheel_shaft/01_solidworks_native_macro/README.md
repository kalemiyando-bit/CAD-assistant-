# SolidWorks gear, wheel, and shaft macro test

This is a **SolidWorks VBA macro source file**. When run inside SolidWorks, it is intended to create:

- `Shaft_12x100.SLDPRT` — circular shaft, Ø12 × 100 mm
- `SpurGear_18T_Module2.SLDPRT` — 18-tooth, module-2 spur gear, 15 mm face width, Ø12 mm bore
- `Wheel_OD80_Hub30.SLDPRT` — Ø80 mm wheel, 24 mm rim width, Ø30 mm hub with 8 mm projection, Ø12 mm bore
- `GearWheelShaftDemo.SLDASM` — all three components positioned coaxially on the shaft
- `.STEP` exports of the three parts and assembly, if the installed SolidWorks STEP exporter accepts the macro's export call

## Run it

1. In SolidWorks, create a new macro using **Tools → Macro → New** and save the macro project.
2. In the VBA editor, use **File → Import File** and select `GenerateGearWheelShaftDemo.bas`.
3. Run `main`.
4. Enter an existing folder when prompted. The macro creates a timestamped subfolder there.

SolidWorks must have default **part** and **assembly** templates configured. The macro uses the English name `Front Plane`; localized SolidWorks installations may require changing that name in the source.

## Demo limitations

- The gear is an editable sketch-and-extrude part, but its involute-like tooth flanks are made from short straight segments. It is **not a production gear profile** and has no strength, wear, backlash, or meshing validation.
- The wheel is a simple rigid demonstration part, not a tire/material model.
- The shaft, gear, and wheel have matching nominal 12 mm bores/diameter. No keyway, retaining hardware, bearings, or mates are included.
- The assembly stores the components at their demonstration positions. The parts are not mechanically constrained by mates.
- The macro source has not been executed in SolidWorks in this environment. SolidWorks API behavior can vary by version; if it reports an error, the exact message and SolidWorks version will help identify the required adjustment.

All dimensions are **test geometry only**, not validated V1 robot specifications.
