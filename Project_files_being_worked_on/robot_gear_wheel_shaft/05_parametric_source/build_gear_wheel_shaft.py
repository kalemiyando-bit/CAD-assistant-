"""Build the demo gear, wheel, shaft, and exchange-format files with CadQuery.

This script writes STEP, STL, 3MF, and DXF outputs into sibling method folders.
Dimensions are demonstration values, not a validated robot drivetrain design.
"""

from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq
import ezdxf


# Shared demo dimensions (millimetres)
GEAR_TEETH = 18
GEAR_MODULE = 2.0
GEAR_PRESSURE_ANGLE_DEG = 20.0
GEAR_FACE_WIDTH = 15.0
GEAR_BORE = 12.0

WHEEL_OD = 80.0
WHEEL_WIDTH = 24.0
WHEEL_HUB_OD = 30.0
WHEEL_HUB_EXTRA = 8.0
WHEEL_BORE = 12.0

SHAFT_DIAMETER = 12.0
SHAFT_LENGTH = 100.0

GEAR_Z = 10.0
WHEEL_Z = 55.0

ROOT = Path(__file__).resolve().parents[1]
STEP_DIR = ROOT / "02_step_exchange"
MESH_DIR = ROOT / "03_mesh_formats"
DXF_DIR = ROOT / "04_dxf_2d"
PI = math.pi


def involute_angle(radius: float, base_radius: float) -> float:
    alpha = math.acos(base_radius / radius)
    return math.tan(alpha) - alpha


def gear_outline_points(
    tooth_count: int = GEAR_TEETH,
    module: float = GEAR_MODULE,
    pressure_angle_deg: float = GEAR_PRESSURE_ANGLE_DEG,
    samples_per_flank: int = 8,
) -> list[tuple[float, float]]:
    """Return a closed, sampled involute-like gear outline in the XY plane."""
    if tooth_count < 8 or module <= 0:
        raise ValueError("Use at least 8 teeth and a positive module.")

    root_radius = (tooth_count - 2.5) * module / 2
    pitch_radius = tooth_count * module / 2
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle_deg))
    outside_radius = (tooth_count + 2) * module / 2
    pressure_angle = math.radians(pressure_angle_deg)
    half_base_angle = (
        PI / (2 * tooth_count) + math.tan(pressure_angle) - pressure_angle
    )
    root_half_angle = math.radians(8)
    half_tip_angle = half_base_angle - involute_angle(
        outside_radius, base_radius
    )

    points: list[tuple[float, float]] = []

    def polar(radius: float, angle: float) -> tuple[float, float]:
        return radius * math.cos(angle), radius * math.sin(angle)

    for tooth in range(tooth_count):
        center = 2 * PI * tooth / tooth_count
        points.append(polar(root_radius, center - root_half_angle))
        points.append(polar(base_radius, center - half_base_angle))

        for sample in range(1, samples_per_flank + 1):
            radius = base_radius + (
                outside_radius - base_radius
            ) * sample / samples_per_flank
            flank_angle = (
                center
                - half_base_angle
                + involute_angle(radius, base_radius)
            )
            points.append(polar(radius, flank_angle))

        points.append(polar(outside_radius, center + half_tip_angle))

        for sample in range(samples_per_flank - 1, -1, -1):
            radius = base_radius + (
                outside_radius - base_radius
            ) * sample / samples_per_flank
            flank_angle = (
                center
                + half_base_angle
                - involute_angle(radius, base_radius)
            )
            points.append(polar(radius, flank_angle))

        points.append(polar(root_radius, center + root_half_angle))

    return points


def make_gear() -> cq.Solid:
    outline = cq.Workplane("XY").polyline(gear_outline_points()).close().val()
    bore = cq.Wire.makeCircle(
        GEAR_BORE / 2, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1)
    )
    return cq.Solid.extrudeLinear(
        outline, [bore], cq.Vector(0, 0, GEAR_FACE_WIDTH)
    )


def make_wheel() -> cq.Solid:
    rim = (
        cq.Workplane("XY")
        .circle(WHEEL_OD / 2)
        .circle(WHEEL_BORE / 2)
        .extrude(WHEEL_WIDTH)
        .val()
    )
    hub = (
        cq.Workplane("XY", origin=(0, 0, WHEEL_WIDTH))
        .circle(WHEEL_HUB_OD / 2)
        .circle(WHEEL_BORE / 2)
        .extrude(WHEEL_HUB_EXTRA)
        .val()
    )
    fused = rim.fuse(hub).clean()
    solids = fused.Solids()
    if len(solids) != 1:
        raise RuntimeError(f"Wheel should be one solid; found {len(solids)}.")
    return solids[0]


def make_shaft() -> cq.Solid:
    return (
        cq.Workplane("XY")
        .circle(SHAFT_DIAMETER / 2)
        .extrude(SHAFT_LENGTH)
        .val()
    )


def export_step_parts(gear: cq.Solid, wheel: cq.Solid, shaft: cq.Solid) -> None:
    cq.exporters.export(
        gear, str(STEP_DIR / "SpurGear_18T_Module2.step"), exportType="STEP"
    )
    cq.exporters.export(
        wheel, str(STEP_DIR / "Wheel_OD80_Hub30.step"), exportType="STEP"
    )
    cq.exporters.export(
        shaft, str(STEP_DIR / "Shaft_12x100.step"), exportType="STEP"
    )

    assembly = cq.Assembly(name="GearWheelShaftDemo")
    assembly.add(shaft, name="Shaft")
    assembly.add(
        gear,
        loc=cq.Location(cq.Vector(0, 0, GEAR_Z)),
        name="Spur gear",
    )
    assembly.add(
        wheel,
        loc=cq.Location(cq.Vector(0, 0, WHEEL_Z)),
        name="Wheel",
    )
    assembly.save(
        str(STEP_DIR / "GearWheelShaftDemo_assembly.step"),
        exportType="STEP",
    )


def export_meshes(gear: cq.Solid, wheel: cq.Solid, shaft: cq.Solid) -> None:
    parts = {
        "SpurGear_18T_Module2": gear,
        "Wheel_OD80_Hub30": wheel,
        "Shaft_12x100": shaft,
    }

    for name, shape in parts.items():
        cq.exporters.export(
            shape,
            str(MESH_DIR / f"{name}.stl"),
            exportType="STL",
            tolerance=0.05,
            angularTolerance=0.08,
            unit="MM",
        )
        cq.exporters.export(
            shape,
            str(MESH_DIR / f"{name}.3mf"),
            exportType="3MF",
            tolerance=0.05,
            angularTolerance=0.08,
            unit="MM",
        )

    compound = cq.Compound.makeCompound(
        [
            shaft,
            gear.translate(cq.Vector(0, 0, GEAR_Z)),
            wheel.translate(cq.Vector(0, 0, WHEEL_Z)),
        ]
    )
    cq.exporters.export(
        compound,
        str(MESH_DIR / "GearWheelShaftDemo_assembly.stl"),
        exportType="STL",
        tolerance=0.05,
        angularTolerance=0.08,
        unit="MM",
    )
    cq.exporters.export(
        compound,
        str(MESH_DIR / "GearWheelShaftDemo_assembly.3mf"),
        exportType="3MF",
        tolerance=0.05,
        angularTolerance=0.08,
        unit="MM",
    )


def new_dxf():
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = ezdxf.units.MM
    doc.header["$MEASUREMENT"] = 1
    for layer, color in [
        ("OUTLINE", 7),
        ("CENTER", 4),
        ("REFERENCE", 8),
        ("LABEL", 2),
    ]:
        doc.layers.new(layer, dxfattribs={"color": color})
    return doc, doc.modelspace()


def add_text(msp, x: float, y: float, value: str, height: float = 3.0) -> None:
    msp.add_text(
        value,
        dxfattribs={"height": height, "layer": "LABEL"},
    ).set_placement((x, y))


def add_rect(msp, x: float, y: float, width: float, height: float) -> None:
    msp.add_lwpolyline(
        [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        ],
        close=True,
        dxfattribs={"layer": "OUTLINE"},
    )


def add_dimension_line(
    msp, x1: float, y1: float, x2: float, y2: float, label: str, tx: float, ty: float
) -> None:
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "REFERENCE"})
    add_text(msp, tx, ty, label, 2.5)


def export_dxfs(gear_points: list[tuple[float, float]]) -> None:
    # Gear top/profile view with reference pitch and root circles.
    doc, msp = new_dxf()
    msp.add_lwpolyline(
        gear_points, close=True, dxfattribs={"layer": "OUTLINE"}
    )
    msp.add_circle((0, 0), GEAR_TEETH * GEAR_MODULE / 2,
                   dxfattribs={"layer": "REFERENCE"})
    msp.add_circle(
        (0, 0),
        (GEAR_TEETH - 2.5) * GEAR_MODULE / 2,
        dxfattribs={"layer": "REFERENCE"},
    )
    msp.add_circle((0, 0), GEAR_BORE / 2, dxfattribs={"layer": "OUTLINE"})
    add_text(msp, -25, -30, "18T MODULE 2 / PA 20 DEG / FACE 15")
    add_text(msp, -25, -35, "OD 40 / ROOT 31 / BORE 12 MM", 2.5)
    add_dimension_line(msp, -20, 24, 20, 24, "OD 40", -4, 26)
    doc.saveas(DXF_DIR / "SpurGear_18T_Module2_profile.dxf")

    # Wheel front and side reference views.
    doc, msp = new_dxf()
    msp.add_circle((40, 40), WHEEL_OD / 2, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((40, 40), WHEEL_HUB_OD / 2, dxfattribs={"layer": "OUTLINE"})
    msp.add_circle((40, 40), WHEEL_BORE / 2, dxfattribs={"layer": "OUTLINE"})
    add_text(msp, 0, 88, "WHEEL FRONT: OD 80 / HUB OD 30 / BORE 12")
    add_rect(msp, 110, 0, WHEEL_WIDTH, WHEEL_OD)
    add_rect(msp, 110 + WHEEL_WIDTH, 25, WHEEL_HUB_EXTRA, WHEEL_HUB_OD)
    add_text(msp, 110, 88, "WHEEL SIDE: RIM 24 WIDE / HUB +8")
    doc.saveas(DXF_DIR / "Wheel_OD80_Hub30_views.dxf")

    # Shaft side view and end view.
    doc, msp = new_dxf()
    add_rect(msp, 0, 0, SHAFT_LENGTH, SHAFT_DIAMETER)
    msp.add_line((0, SHAFT_DIAMETER / 2), (SHAFT_LENGTH, SHAFT_DIAMETER / 2),
                 dxfattribs={"layer": "CENTER"})
    msp.add_circle((120, SHAFT_DIAMETER / 2), SHAFT_DIAMETER / 2,
                   dxfattribs={"layer": "OUTLINE"})
    add_text(msp, 0, 18, "SHAFT SIDE: DIA 12 x 100")
    add_text(msp, 105, 18, "END")
    doc.saveas(DXF_DIR / "Shaft_12x100_views.dxf")

    # Side-layout reference for the positioned three-part demo assembly.
    doc, msp = new_dxf()
    add_rect(msp, 0, -SHAFT_DIAMETER / 2, SHAFT_LENGTH, SHAFT_DIAMETER)
    add_rect(
        msp,
        GEAR_Z,
        -(GEAR_TEETH * GEAR_MODULE + 4 * GEAR_MODULE) / 2,
        GEAR_FACE_WIDTH,
        (GEAR_TEETH + 2) * GEAR_MODULE,
    )
    add_rect(msp, WHEEL_Z, -WHEEL_OD / 2, WHEEL_WIDTH, WHEEL_OD)
    add_rect(
        msp,
        WHEEL_Z + WHEEL_WIDTH,
        -WHEEL_HUB_OD / 2,
        WHEEL_HUB_EXTRA,
        WHEEL_HUB_OD,
    )
    add_text(msp, 0, 48, "ASSEMBLY SIDE LAYOUT - SHAFT AXIS Z")
    add_text(msp, GEAR_Z, -28, "GEAR @ 10 mm", 2.5)
    add_text(msp, WHEEL_Z, -48, "WHEEL @ 55 mm", 2.5)
    add_text(msp, 0, -56, "POSITIONS ARE DEMO VALUES; NO MATES OR RETAINERS", 2.5)
    doc.saveas(DXF_DIR / "GearWheelShaftDemo_assembly_layout.dxf")


def validate(name: str, shape: cq.Shape) -> None:
    if not shape.isValid():
        raise RuntimeError(f"{name} failed the CAD-kernel validity check.")
    if len(shape.Solids()) != 1:
        raise RuntimeError(f"{name} should contain one solid.")
    box = shape.BoundingBox()
    print(
        f"{name}: valid one-solid model; "
        f"bounds {box.xlen:.3f} x {box.ylen:.3f} x {box.zlen:.3f} mm; "
        f"volume {shape.Volume():.2f} mm^3"
    )


def main() -> None:
    for folder in (STEP_DIR, MESH_DIR, DXF_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    gear = make_gear()
    wheel = make_wheel()
    shaft = make_shaft()
    validate("Gear", gear)
    validate("Wheel", wheel)
    validate("Shaft", shaft)

    export_step_parts(gear, wheel, shaft)
    export_meshes(gear, wheel, shaft)
    export_dxfs(gear_outline_points())
    print(f"Generated format comparison under: {ROOT}")


if __name__ == "__main__":
    main()
