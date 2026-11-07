# STEP exchange method

Contains individual STEP solids for the gear, wheel, and shaft, plus an assembly STEP containing their positioned geometry.

Open `GearWheelShaftDemo_assembly.step` first to test assembly import. If SolidWorks imports it as one multibody part instead of an assembly tree, open the individual STEP files and create an assembly from those parts; the native macro method is intended to create `.SLDASM` directly.

STEP preserves the modeled boundary geometry and units, but not the CadQuery or SolidWorks sketch/feature history. The assembly placements match the demo values in the package-level README.

The gear is a sampled polygonal approximation of an involute-like outline, not a production gear design.
