"""Generate preliminary Robot V1 concept geometry and SolidWorks exchange files.

All dimensions are millimetres. The geometry is a packaging concept, not a
manufacturing release. Purchased components are envelope blocks unless stated
otherwise. See the package registers before using any model for fabrication.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import cadquery as cq
import ezdxf


ROOT = Path(__file__).resolve().parents[1]
STEP_ROOT = ROOT / "18_STEP_Only"
MM = 1.0

FOLDERS = {
    "overall": ROOT / "01_Overall_Concept",
    "chassis": ROOT / "02_Chassis",
    "mobility": ROOT / "03_Mobility_and_Drive",
    "gears": ROOT / "04_Gear_Train",
    "power": ROOT / "05_Power_and_Electronics",
    "sensors": ROOT / "06_Sensors_and_Navigation",
    "loader": ROOT / "07_Loader_Assembly",
    "winch": ROOT / "08_Winch_and_Lifting",
    "shovel": ROOT / "09_Shovel_and_Load_Measurement",
    "tray": ROOT / "10_Tray_and_Enclosure",
    "parts": ROOT / "11_SolidWorks_Parts",
    "assemblies": ROOT / "12_SolidWorks_Assemblies",
    "drawings": ROOT / "13_Engineering_Drawings",
    "calcs": ROOT / "14_Calculations_and_BOM",
    "videos": ROOT / "15_Videos_and_Animations",
    "testing": ROOT / "16_Testing_and_Validation",
}

# Master dimensions, chosen to satisfy the initial brief targets where possible.
FRAME_L = 800.0
FRAME_W = 450.0
FRAME_TUBE = 30.0
FRAME_BOTTOM_Z = 30.0
FRAME_CZ = FRAME_BOTTOM_Z + FRAME_TUBE / 2
DECK_Z = FRAME_BOTTOM_Z + FRAME_TUBE
WHEEL_D = 150.0
WHEEL_R = WHEEL_D / 2
WHEEL_WIDTH = 36.0
WHEELBASE = 640.0
TRACK = 380.0
WHEEL_X = WHEELBASE / 2
WHEEL_Y = TRACK / 2
WHEEL_CZ = WHEEL_R
CASTER_D = 90.0
CASTER_R = CASTER_D / 2
TRAY_L = 600.0
TRAY_W = 400.0
TRAY_FLOOR_Z = 740.0
TRAY_LIP_H = 40.0
LOADER_PIVOT = (160.0, 0.0, 190.0)
LOADER_ARM_L = 600.0
LOADER_PICKUP_DEG = -15.0
LOADER_TRAY_DEG = 75.0
GEAR_MODULE = 2.0
GEAR_PA_DEG = 20.0
GEAR_FACE = 20.0
GEAR_TEETH = (18, 36, 54)
GEAR_CENTER_X = (0.0, 54.0, 144.0)
PI = math.pi


@dataclass
class PartMeta:
    name: str
    subsystem: str
    material: str
    status: str
    note: str


PARTS: dict[str, cq.Shape] = {}
PART_META: dict[str, PartMeta] = {}
INSTANCES: list[tuple[cq.Shape, str, str]] = []
SUBSYSTEM_INSTANCES: dict[str, list[tuple[cq.Shape, str]]] = {}
COUNTS: dict[str, int] = {}
INSTANCE_COUNTS: dict[str, int] = {}


def v(x: float, y: float, z: float) -> cq.Vector:
    return cq.Vector(float(x), float(y), float(z))


def box(lx: float, ly: float, lz: float) -> cq.Shape:
    return cq.Workplane("XY").box(lx, ly, lz).val()


def centered_cylinder_z(radius: float, length: float) -> cq.Shape:
    return cq.Workplane("XY").circle(radius).extrude(length).translate(
        (0, 0, -length / 2)
    ).val()


def ring_z(outer_radius: float, inner_radius: float, length: float) -> cq.Shape:
    return (
        cq.Workplane("XY")
        .circle(outer_radius)
        .circle(inner_radius)
        .extrude(length)
        .translate((0, 0, -length / 2))
        .val()
    )


def cylinder_y(radius: float, length: float) -> cq.Shape:
    return centered_cylinder_z(radius, length).rotate(
        (0, 0, 0), (1, 0, 0), 90
    )


def tube_x(length: float, section: float = 30.0, wall: float = 2.0) -> cq.Shape:
    outer = box(length, section, section)
    inner = box(length + 2, section - 2 * wall, section - 2 * wall)
    return outer.cut(inner)


def tube_y(length: float, section: float = 30.0, wall: float = 2.0) -> cq.Shape:
    return tube_x(length, section, wall).rotate(
        (0, 0, 0), (0, 0, 1), 90
    )


def tube_z(length: float, section: float = 20.0, wall: float = 2.0) -> cq.Shape:
    outer = box(section, section, length)
    inner = box(section - 2 * wall, section - 2 * wall, length + 2)
    return outer.cut(inner)


def xz_plate(
    length_x: float,
    length_z: float,
    thickness_y: float,
    holes: list[tuple[float, float, float]] | None = None,
) -> cq.Shape:
    plate = box(length_x, thickness_y, length_z)
    for hx, hz, radius in holes or []:
        cutter = cq.Solid.makeCylinder(
            radius,
            thickness_y + 2,
            v(hx, -thickness_y / 2 - 1, hz),
            v(0, 1, 0),
        )
        plate = plate.cut(cutter)
    return plate


def make_gear(
    teeth: int,
    module: float = GEAR_MODULE,
    face_width: float = GEAR_FACE,
    bore: float = 12.0,
    pressure_angle_deg: float = GEAR_PA_DEG,
) -> cq.Solid:
    """Sampled involute-like spur gear for packaging; not a production tooth form."""
    if teeth < 8:
        raise ValueError("The concept gear generator requires at least 8 teeth.")
    rp = teeth * module / 2
    rb = rp * math.cos(math.radians(pressure_angle_deg))
    ra = (teeth + 2) * module / 2
    rf = (teeth - 2.5) * module / 2
    pa = math.radians(pressure_angle_deg)
    half_base = PI / (2 * teeth) + math.tan(pa) - pa
    half_tip = half_base - (
        math.tan(math.acos(rb / ra)) - math.acos(rb / ra)
    )
    half_root = PI * 0.75 / teeth
    points: list[tuple[float, float]] = []

    def point(radius: float, angle: float) -> tuple[float, float]:
        return radius * math.cos(angle), radius * math.sin(angle)

    def inv_at(radius: float) -> float:
        alpha = math.acos(rb / radius)
        return math.tan(alpha) - alpha

    for tooth in range(teeth):
        center = tooth * 2 * PI / teeth
        points.append(point(rf, center - half_root))
        points.append(point(rb, center - half_base))
        for sample in range(1, 7):
            radius = rb + (ra - rb) * sample / 6
            points.append(point(radius, center - half_base + inv_at(radius)))
        points.append(point(ra, center + half_tip))
        for sample in range(5, -1, -1):
            radius = rb + (ra - rb) * sample / 6
            points.append(point(radius, center + half_base - inv_at(radius)))
        points.append(point(rf, center + half_root))

    outer = cq.Workplane("XY").polyline(points).close().val()
    inner = cq.Wire.makeCircle(
        bore / 2, v(0, 0, 0), v(0, 0, 1)
    )
    return cq.Solid.extrudeLinear(
        outer,
        [inner],
        v(0, 0, face_width),
    ).translate(v(0, 0, -face_width / 2))


def make_wheel_tire() -> cq.Solid:
    outer = centered_cylinder_z(WHEEL_R, WHEEL_WIDTH)
    inner = centered_cylinder_z(44.0, WHEEL_WIDTH + 2)
    return outer.cut(inner)


def make_wheel_disc() -> cq.Solid:
    disc = ring_z(45.0, 15.0, 4.0)
    for index in range(6):
        angle = 2 * PI * index / 6
        cutter = cq.Solid.makeCylinder(
            3.3,
            6,
            v(34 * math.cos(angle), 34 * math.sin(angle), -3),
            v(0, 0, 1),
        )
        disc = disc.cut(cutter)
    return disc


def make_passive_wheel() -> cq.Solid:
    return ring_z(CASTER_R, 10.0, 25.0)


def make_front_enclosure_panel() -> cq.Shape:
    panel = box(2.0, 270.0, 190.0)
    # Clearance slots for the pair of loader arms as they sweep through the panel.
    for y in (-100.0, 100.0):
        panel = panel.cut(box(4.0, 52.0, 150.0).translate((0, y, 35.0)))
    return panel


def make_cable_sector() -> cq.Shape:
    outer_r, inner_r = 150.0, 20.0
    start_deg, end_deg = -25.0, 90.0
    points = []
    for i in range(25):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / 24)
        points.append((outer_r * math.cos(angle), outer_r * math.sin(angle)))
    for i in range(24, -1, -1):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / 24)
        points.append((inner_r * math.cos(angle), inner_r * math.sin(angle)))
    return (
        cq.Workplane("XY")
        .polyline(points)
        .close()
        .extrude(8.0)
        .translate((0, 0, -4.0))
        .val()
    )


def make_deck_plate() -> cq.Shape:
    plate = box(FRAME_L, FRAME_W, 3.0)
    for x in (-WHEEL_X, WHEEL_X):
        for y in (-WHEEL_Y, WHEEL_Y):
            # Open-ended relief slots keep the upper plate clear of the wheel envelopes.
            plate = plate.cut(box(160.0, 50.0, 6.0).translate((x, y, 0)))
    return plate


def make_gearbox_plate(x_positions: tuple[float, float, float]) -> cq.Shape:
    holes = [
        (x_positions[0], 0, 6.0),
        (x_positions[1], 0, 7.0),
        (x_positions[2], 0, 8.5),
    ]
    plate = xz_plate(165.0, 126.0, 4.0, holes)
    return plate


def make_hub() -> cq.Solid:
    return ring_z(15.0, 7.5, 52.0)


def make_caster_fork() -> cq.Shape:
    left = box(8.0, 10.0, 55.0).translate((-10.0, -14.0, -27.5))
    right = box(8.0, 10.0, 55.0).translate((-10.0, 14.0, -27.5))
    crown = box(35.0, 38.0, 6.0).translate((0, 0, -3.0))
    axle = cylinder_y(6.0, 36.0).translate((-10.0, 0, -55.0))
    return left.fuse(right).fuse(crown).fuse(axle).clean()


def make_bucket() -> cq.Shape:
    # Front edge is at local x=0; the bucket body extends rearward to -180.
    floor = box(180.0, 300.0, 3.0).translate((-90.0, 0, -28.5))
    back_lip = box(3.0, 300.0, 30.0).translate((-178.5, 0, -13.0))
    front_hook = box(3.0, 300.0, 58.0).translate((-1.5, 0, 0.0))
    side_l = box(180.0, 3.0, 58.0).translate((-90.0, -148.5, 0.0))
    side_r = box(180.0, 3.0, 58.0).translate((-90.0, 148.5, 0.0))
    return floor.fuse(back_lip).fuse(front_hook).fuse(side_l).fuse(side_r).clean()


def make_tray_floor() -> cq.Shape:
    return box(TRAY_L, TRAY_W, 3.0)


def make_tray_lip(length: float, height: float) -> cq.Shape:
    return box(length, 3.0, height)


def make_motor_envelope() -> cq.Shape:
    motor = centered_cylinder_z(34.0, 92.0)
    gearbox = box(72.0, 72.0, 32.0).translate((0, 0, 55.0))
    shaft = centered_cylinder_z(5.0, 25.0).translate((0, 0, 82.0))
    return motor.fuse(gearbox).fuse(shaft).clean()


def make_linear_actuator_envelope() -> cq.Shape:
    housing = centered_cylinder_z(14.0, 175.0)
    rod = centered_cylinder_z(7.0, 150.0).translate((0, 0, 150.0))
    eye1 = centered_cylinder_z(10.0, 12.0).translate((0, 0, -90.0))
    eye2 = centered_cylinder_z(10.0, 12.0).translate((0, 0, 225.0))
    return housing.fuse(rod).fuse(eye1).fuse(eye2).clean()


def register(
    name: str,
    shape: cq.Shape,
    subsystem: str,
    material: str,
    status: str = "PRELIMINARY",
    note: str = "",
) -> cq.Shape:
    if name in PARTS:
        return PARTS[name]
    PARTS[name] = shape
    PART_META[name] = PartMeta(name, subsystem, material, status, note)
    return shape


def located(
    shape: cq.Shape,
    xyz: tuple[float, float, float],
    rotation_axis: tuple[float, float, float] | None = None,
    rotation_deg: float = 0.0,
) -> cq.Shape:
    moved = shape
    if rotation_axis is not None and abs(rotation_deg) > 1e-8:
        moved = moved.rotate((0, 0, 0), rotation_axis, rotation_deg)
    return moved.translate(v(*xyz))


def place(
    part_name: str,
    subsystem: str,
    shape: cq.Shape,
    xyz: tuple[float, float, float],
    rotation_axis: tuple[float, float, float] | None = None,
    rotation_deg: float = 0.0,
    part_key: str | None = None,
) -> cq.Shape:
    world_shape = located(shape, xyz, rotation_axis, rotation_deg)
    INSTANCE_COUNTS[part_name] = INSTANCE_COUNTS.get(part_name, 0) + 1
    instance_name = f"{part_name}_{INSTANCE_COUNTS[part_name]:02d}"
    if part_key is None:
        part_key = next((key for key, value in PARTS.items() if value is shape), None)
    if part_key:
        COUNTS[part_key] = COUNTS.get(part_key, 0) + 1
    INSTANCES.append((world_shape, instance_name, subsystem))
    SUBSYSTEM_INSTANCES.setdefault(subsystem, []).append((world_shape, instance_name))
    return world_shape


def cylinder_between(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
) -> cq.Solid:
    a, b = v(*start), v(*end)
    delta = b.sub(a)
    return cq.Solid.makeCylinder(radius, delta.Length, a, delta.normalized())


def align_local_z(
    shape: cq.Shape,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    local_start_z: float = 0.0,
) -> cq.Shape:
    dx, dy, dz = (end[i] - start[i] for i in range(3))
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length <= 1e-9:
        raise ValueError("Alignment points must be distinct.")
    ux, uy, uz = dx / length, dy / length, dz / length
    axis = (-uy, ux, 0.0)
    axis_length = math.sqrt(axis[0] * axis[0] + axis[1] * axis[1])
    angle = math.degrees(math.acos(max(-1.0, min(1.0, uz))))
    if axis_length <= 1e-9:
        axis = (1.0, 0.0, 0.0)
    moved = shape.rotate((0, 0, 0), axis, angle)
    offset = (
        start[0] - local_start_z * ux,
        start[1] - local_start_z * uy,
        start[2] - local_start_z * uz,
    )
    return moved.translate(v(*offset))


def build_parts() -> None:
    # Primary structure.
    register(
        "Frame_Rail_30x30x800",
        tube_x(FRAME_L),
        "Chassis",
        "6061-T6 aluminium extrusion (recommendation)",
        note="30x30x2 mm hollow envelope; extrusion supplier profile must be confirmed.",
    )
    register(
        "Crossmember_30x30x450",
        tube_y(FRAME_W),
        "Chassis",
        "6061-T6 aluminium extrusion (recommendation)",
    )
    register(
        "Crossmember_30x30x220",
        tube_y(220.0),
        "Chassis",
        "6061-T6 aluminium extrusion (recommendation)",
    )
    register(
        "Deck_Plate_800x450x3",
        make_deck_plate(),
        "Chassis",
        "5052-H32 aluminium sheet (recommendation)",
        note="Wheel relief slots are packaging cutouts; confirm edge distances and reinforcement.",
    )
    register(
        "Wheel_Module_Outrigger",
        box(120.0, 30.0, 8.0),
        "Chassis",
        "6061-T6 aluminium plate (recommendation)",
    )
    register(
        "Loader_Pivot_Gusset",
        xz_plate(200.0, 200.0, 8.0, [(0.0, 60.0, 10.0)]),
        "Loader",
        "6061-T6 aluminium plate (recommendation)",
        note="Concept pivot bracket; thickness, fastener group, and load transfer must be calculated.",
    )
    register(
        "Bumper_Beam_820x30x25",
        box(25.0, 420.0, 30.0),
        "Chassis",
        "Aluminium backing beam with elastomer bumper (recommendation)",
    )

    # Mobility and three-gear drive.
    register(
        "Drive_Tire_OD150_W36",
        make_wheel_tire(),
        "Mobility",
        "Solid rubber or polyurethane tread (supplier-dependent)",
        note="Annular envelope, not a selected tire profile.",
    )
    register(
        "Drive_Wheel_Disc_OD90",
        make_wheel_disc(),
        "Mobility",
        "6061-T6 aluminium plate (recommendation)",
        note="Six 6.6 mm bolt holes on 68 mm PCD; confirm hub interface.",
    )
    register(
        "Drive_Wheel_Hub_OD30",
        make_hub(),
        "Mobility",
        "1045 steel or 6061-T6 aluminium (supplier/design-dependent)",
        note="52 mm long, 15 mm nominal bore; key, clamp, and fit remain to be selected.",
    )
    register(
        "Passive_Caster_Wheel_OD90",
        make_passive_wheel(),
        "Mobility",
        "Polyurethane tread with polymer/metal hub (supplier-dependent)",
    )
    register(
        "Passive_Caster_Fork",
        make_caster_fork(),
        "Mobility",
        "Steel plate fabrication (recommendation)",
        note="Fork geometry is an envelope; swivel bearing and trail require supplier selection.",
    )
    register(
        "Steering_Bearing_Envelope",
        ring_z(40.0, 25.0, 12.0),
        "Mobility",
        "Purchased slewing/thrust bearing (supplier-dependent)",
    )
    register(
        "Drive_Steering_Servo_Envelope",
        box(58.0, 48.0, 42.0),
        "Mobility",
        "Purchased 24 V steering actuator envelope",
        status="SUPPLIER-DEPENDENT",
        note="Required output torque, duty, backlash, and feedback must be selected.",
    )
    register(
        "Drive_Gearmotor_24V_230RPM_Envelope",
        make_motor_envelope(),
        "Mobility",
        "Purchased 24 V DC/BLDC gearmotor envelope",
        status="SUPPLIER-DEPENDENT",
        note="Target output 225-240 rpm and about 2 N·m continuous at the 18T pinion; not a selected motor.",
    )
    for teeth, bore in zip(GEAR_TEETH, (10.0, 12.0, 15.0)):
        register(
            f"Spur_Gear_{teeth}T_M2",
            make_gear(teeth, bore=bore),
            "GearTrain",
            "Steel spur gear, module 2, 20° pressure angle (recommendation)",
            note="Sampled involute-like CAD outline; replace with supplier/manufacturing-validated tooth geometry.",
        )
    register(
        "Gearbox_Side_Plate_Front",
        make_gearbox_plate((-72.0, -18.0, 72.0)),
        "GearTrain",
        "6061-T6 aluminium plate, 4 mm (recommendation)",
        note="Bearing holes are conceptual; select bearings and add tolerances.",
    )
    register(
        "Gearbox_Side_Plate_Rear",
        make_gearbox_plate((72.0, 18.0, -72.0)),
        "GearTrain",
        "6061-T6 aluminium plate, 4 mm (recommendation)",
    )
    register(
        "Pinion_Shaft_D10",
        cylinder_y(5.0, 42.0),
        "GearTrain",
        "1045 steel (recommendation)",
        note="10 mm nominal shaft; key/flat and bearing fits remain to be detailed.",
    )
    register(
        "Idler_Shaft_D12",
        cylinder_y(6.0, 48.0),
        "GearTrain",
        "1045 steel (recommendation)",
    )
    register(
        "Wheel_Output_Shaft_D15",
        cylinder_y(7.5, 70.0),
        "GearTrain",
        "1045 steel (recommendation)",
        note="15 mm nominal shaft; check bending, key, and bearing life.",
    )
    register(
        "Gearbox_Guard_Panel",
        box(170.0, 35.0, 135.0),
        "GearTrain",
        "1.5 mm formed aluminium or steel guard (recommendation)",
    )

    # Enclosure, power, and purchased electronic envelopes.
    register("Enclosure_Floor_720x270x2", box(720, 270, 2), "Power", "5052-H32 aluminium sheet")
    register("Enclosure_Side_Panel_720x190x2", box(720, 2, 190), "Power", "5052-H32 aluminium sheet")
    register("Enclosure_Rear_Panel_270x190x2", box(2, 270, 190), "Power", "5052-H32 aluminium sheet")
    register("Enclosure_Front_Panel_Loader_Slots", make_front_enclosure_panel(), "Power", "5052-H32 aluminium sheet")
    register("Enclosure_Top_Cover_720x270x2", box(720, 270, 2), "Power", "5052-H32 aluminium sheet")
    register(
        "Battery_24V_15Ah_Envelope",
        box(240, 150, 125),
        "Power",
        "Purchased LiFePO4 battery envelope",
        status="SUPPLIER-DEPENDENT",
        note="24 V nominal, 15 Ah target; verify BMS, current, chemistry, mass, and dimensions.",
    )
    register(
        "Motor_Controller_Envelope",
        box(120, 90, 32),
        "Power",
        "Purchased dual-channel motor controller envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register(
        "Compute_Board_Envelope",
        box(100, 80, 24),
        "Power",
        "Purchased controller/computer envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register(
        "Power_Distribution_Box_Envelope",
        box(100, 80, 45),
        "Power",
        "Purchased fused distribution and isolation envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register("Electronics_Mounting_Tray", box(260, 220, 2), "Power", "5052-H32 aluminium sheet")
    register("Battery_Hold_Down_Bar", box(250, 18, 4), "Power", "6061-T6 aluminium plate")

    # Sensors and operator interface.
    register(
        "Line_Sensor_Array_100x14",
        box(100, 14, 10),
        "Sensors",
        "Purchased reflectance sensor array envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register(
        "Obstacle_Sensor_Envelope",
        box(42, 28, 22),
        "Sensors",
        "Purchased time-of-flight/ultrasonic envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register(
        "Object_Camera_Envelope",
        box(42, 32, 25),
        "Sensors",
        "Phone camera or compact camera envelope",
        status="SUPPLIER-DEPENDENT",
    )
    register("HMI_Display_Envelope", box(90, 18, 55), "Sensors", "Purchased LCD display envelope")
    register("Emergency_Stop_Envelope", centered_cylinder_z(18, 24), "Sensors", "Purchased latching E-stop")
    register("Phone_Clamp_Assembly", box(84, 26, 165), "Sensors", "Aluminium/printed polymer mount")
    register("Phone_Mount_Arm", box(30, 30, 120), "Sensors", "6061-T6 aluminium arm")
    register("Sensor_Bumper_Bracket", box(50, 30, 35), "Sensors", "5052-H32 aluminium plate")

    # Tray and support structure.
    register("Tray_Floor_600x400x3", make_tray_floor(), "Tray", "5052-H32 aluminium sheet")
    register("Tray_Long_Lip_600x40x3", make_tray_lip(600, 40), "Tray", "5052-H32 aluminium sheet")
    register("Tray_Short_Lip_400x40x3", make_tray_lip(400, 40), "Tray", "5052-H32 aluminium sheet")
    register("Tray_NonSlip_Mat_580x380x2", box(580, 380, 2), "Tray", "Oil-resistant elastomer sheet")
    register(
        "Tray_Support_Post_20x20x480",
        tube_z(480, 20, 2),
        "Tray",
        "6061-T6 aluminium extrusion",
    )
    register("Tray_Corner_Bracket", box(60, 60, 5), "Tray", "6061-T6 aluminium plate")

    # Loader, winch, and load measurement.
    register(
        "Loader_Arm_25x20x600",
        box(LOADER_ARM_L, 25, 20).translate((LOADER_ARM_L / 2, 0, 0)),
        "Loader",
        "6061-T6 aluminium rectangular tube (recommendation)",
        note="Solid envelope in CAD; use hollow tube after bending/deflection checks.",
    )
    register("Loader_Pivot_Cross_Shaft_D20", cylinder_y(10, 250), "Loader", "1045 steel")
    register("Loader_Pivot_Bearing_Envelope", ring_z(20, 10, 12), "Loader", "Purchased bearing/bushing envelope")
    register("Loader_Tip_Crossbar", box(25, 240, 25), "Loader", "6061-T6 aluminium tube")
    register(
        "Cable_Sector_R150",
        make_cable_sector(),
        "Winch",
        "Steel plate sector with cable/chain groove (recommendation)",
        note="Sector groove and end attachment require detailed design.",
    )
    register("Cable_Guide_Sheave_D60", ring_z(30, 6, 16), "Winch", "Purchased sheave envelope")
    register("Winch_Drum_D50_W60", ring_z(25, 8, 60), "Winch", "Steel drum envelope")
    register("Winch_Drum_Flange_D90", ring_z(45, 8, 6), "Winch", "Steel plate")
    register(
        "Winch_Motor_24V_25Nm_Envelope",
        make_motor_envelope(),
        "Winch",
        "Purchased 24 V brake/worm gearmotor envelope",
        status="SUPPLIER-DEPENDENT",
        note="Output target at least 25 N·m with independent load retention; supplier data required.",
    )
    register("Winch_Ratchet_Disc_D90", make_gear(24, module=3.0, face_width=8, bore=12), "Winch", "Steel ratchet disc")
    register("Winch_Pawl", box(45, 12, 18), "Winch", "Steel pawl with return spring (recommendation)")
    register("Cable_LoadCell_1kN_Envelope", box(65, 22, 18), "Shovel", "Purchased tension load cell", status="SUPPLIER-DEPENDENT")
    register("Linear_Actuator_24V_150mm_Envelope", make_linear_actuator_envelope(), "Shovel", "Purchased self-locking linear actuator envelope", status="SUPPLIER-DEPENDENT")
    register("Shovel_Bucket_300x180", make_bucket(), "Shovel", "5052-H32 aluminium sheet, 3 mm (recommendation)")
    register("Shovel_Hinge_Cheek", xz_plate(90, 80, 6, [(0, 0, 8)]), "Shovel", "6061-T6 aluminium plate")
    register("Shovel_Actuator_Bracket", box(50, 35, 6), "Shovel", "6061-T6 aluminium plate")


def add_component(
    name: str,
    subsystem: str,
    part: str,
    xyz: tuple[float, float, float],
    axis: tuple[float, float, float] | None = None,
    angle: float = 0.0,
) -> cq.Shape:
    return place(name, subsystem, PARTS[part], xyz, axis, angle, part_key=part)


def add_y_axis_part(
    name: str,
    subsystem: str,
    part: str,
    xyz: tuple[float, float, float],
) -> cq.Shape:
    return add_component(name, subsystem, part, xyz, (1, 0, 0), 90.0)


def build_assembly_instances() -> None:
    # Chassis frame and deck.
    frame = PARTS["Frame_Rail_30x30x800"]
    for y in (-110.0, 110.0):
        place("Frame_Rail_L", "Chassis", frame, (0, y, FRAME_CZ))
    full_cross = PARTS["Crossmember_30x30x450"]
    place("Crossmember_FullWidth", "Chassis", full_cross, (0.0, 0, FRAME_CZ))
    inner_cross = PARTS["Crossmember_30x30x220"]
    for x in (-250.0, 250.0):
        place("Crossmember_Inner", "Chassis", inner_cross, (x, 0, FRAME_CZ))
    place("Chassis_Deck", "Chassis", PARTS["Deck_Plate_800x450x3"], (0, 0, DECK_Z + 1.5))
    for x in (-320.0, 320.0):
        for y in (-190.0, 190.0):
            place("Wheel_Module_Outrigger", "Chassis", PARTS["Wheel_Module_Outrigger"], (x, math.copysign(125.0, y), 56.0))
    for x in (-410.0, 410.0):
        place("Bumper_Beam", "Chassis", PARTS["Bumper_Beam_820x30x25"], (x, 0, 95.0))

    # Powered diagonal pair: front-left and rear-right. Opposite corners are passive casters.
    tire = PARTS["Drive_Tire_OD150_W36"]
    disc = PARTS["Drive_Wheel_Disc_OD90"]
    hub = PARTS["Drive_Wheel_Hub_OD30"]
    passive = PARTS["Passive_Caster_Wheel_OD90"]
    caster_fork = PARTS["Passive_Caster_Fork"]
    steering_bearing = PARTS["Steering_Bearing_Envelope"]
    steering_servo = PARTS["Drive_Steering_Servo_Envelope"]
    module_locations = [
        ("Front_Left", 320.0, -190.0, -1.0, 1.0),
        ("Rear_Right", -320.0, 190.0, 1.0, -1.0),
    ]
    for tag, x_out, y_wheel, y_sign, x_direction in module_locations:
        # Tire, wheel discs, and hub are coaxial along Y.
        add_y_axis_part(f"{tag}_Drive_Tire", "Mobility", "Drive_Tire_OD150_W36", (x_out, y_wheel, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Wheel_Disc_Inboard", "Mobility", "Drive_Wheel_Disc_OD90", (x_out, y_wheel - y_sign * 15.0, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Wheel_Disc_Outboard", "Mobility", "Drive_Wheel_Disc_OD90", (x_out, y_wheel + y_sign * 15.0, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Wheel_Hub", "Mobility", "Drive_Wheel_Hub_OD30", (x_out, y_wheel, WHEEL_CZ))
        # Gear train center positions are dimensioned from the output wheel axis.
        sign = x_direction
        x_positions = (x_out - sign * 144.0, x_out - sign * 90.0, x_out)
        plate_part = "Gearbox_Side_Plate_Front" if x_direction > 0 else "Gearbox_Side_Plate_Rear"
        x_mid = (x_positions[0] + x_positions[2]) / 2
        for plate_y in (y_sign * 142.0, y_sign * 174.0):
            place(
                f"{tag}_Gearbox_Side_Plate",
                "GearTrain",
                PARTS[plate_part],
                (x_mid, plate_y, WHEEL_CZ),
            )
        gear_names = ("Spur_Gear_18T_M2", "Spur_Gear_36T_M2", "Spur_Gear_54T_M2")
        gear_y = y_sign * 158.0
        for gear_name, gx in zip(gear_names, x_positions):
            add_y_axis_part(f"{tag}_{gear_name}", "GearTrain", gear_name, (gx, gear_y, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Pinion_Shaft", "GearTrain", "Pinion_Shaft_D10", (x_positions[0], gear_y, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Idler_Shaft", "GearTrain", "Idler_Shaft_D12", (x_positions[1], gear_y, WHEEL_CZ))
        add_y_axis_part(f"{tag}_Output_Shaft", "GearTrain", "Wheel_Output_Shaft_D15", (x_out, y_sign * 174.0, WHEEL_CZ))
        place(
            f"{tag}_Drive_Motor",
            "Mobility",
            PARTS["Drive_Gearmotor_24V_230RPM_Envelope"],
            (x_positions[0], y_sign * 224.0, WHEEL_CZ),
            (1, 0, 0),
            90.0 * y_sign,
        )
        # Gear guard sits outside the gear plane; not shown as a detailed formed cover.
        place(f"{tag}_Gearbox_Guard", "GearTrain", PARTS["Gearbox_Guard_Panel"], (x_mid, y_sign * 185.0, WHEEL_CZ))
        place(f"{tag}_Steering_Bearing", "Mobility", PARTS["Steering_Bearing_Envelope"], (x_out, y_wheel, 115.0))
        place(f"{tag}_Steering_Actuator", "Mobility", steering_servo, (x_out - 15.0, y_wheel, 155.0))

    # Passive diagonal casters; trail is toward the rear of each mount in this nominal pose.
    for tag, x, y in (("Front_Right", 320.0, 190.0), ("Rear_Left", -320.0, -190.0)):
        place(f"{tag}_Caster_Fork", "Mobility", caster_fork, (x, y, 92.0))
        add_y_axis_part(f"{tag}_Caster_Wheel", "Mobility", "Passive_Caster_Wheel_OD90", (x - 10.0, y, CASTER_R))
        place(f"{tag}_Caster_Swivel_Bearing", "Mobility", steering_bearing, (x, y, 100.0))

    # Lower electronics enclosure and major purchased envelopes.
    place("Enclosure_Floor", "Power", PARTS["Enclosure_Floor_720x270x2"], (0, 0, 64.0))
    for y in (-135.0, 135.0):
        place("Enclosure_Side_Panel", "Power", PARTS["Enclosure_Side_Panel_720x190x2"], (0, y, 160.0))
    place("Enclosure_Rear_Panel", "Power", PARTS["Enclosure_Rear_Panel_270x190x2"], (-359.0, 0, 160.0))
    place(
        "Enclosure_Front_Panel",
        "Power",
        PARTS["Enclosure_Front_Panel_Loader_Slots"],
        (359.0, 0, 160.0),
    )
    place("Battery_Pack_Envelope", "Power", PARTS["Battery_24V_15Ah_Envelope"], (-110, 0, 132.0))
    place("Battery_Hold_Down", "Power", PARTS["Battery_Hold_Down_Bar"], (-110, 0, 199.0))
    place("Electronics_Tray", "Power", PARTS["Electronics_Mounting_Tray"], (180, 0, 67.0))
    place("Motor_Controller", "Power", PARTS["Motor_Controller_Envelope"], (160, -58, 92.0))
    place("Motor_Controller", "Power", PARTS["Motor_Controller_Envelope"], (160, 58, 92.0))
    place("Compute_Board", "Power", PARTS["Compute_Board_Envelope"], (260, 0, 92.0))
    place("Power_Distribution", "Power", PARTS["Power_Distribution_Box_Envelope"], (-290, 0, 95.0))
    place("Enclosure_Top_Cover", "Power", PARTS["Enclosure_Top_Cover_720x270x2"], (0, 0, 256.0))

    # Tray supports and carrying tray.
    post = PARTS["Tray_Support_Post_20x20x480"]
    for x in (-260.0, 260.0):
        for y in (-175.0, 175.0):
            place("Tray_Support_Post", "Tray", post, (x, y, (260.0 + 740.0) / 2))
            place("Tray_Corner_Bracket", "Tray", PARTS["Tray_Corner_Bracket"], (x, y, 250.0))
    place("Tray_Floor", "Tray", PARTS["Tray_Floor_600x400x3"], (0, 0, TRAY_FLOOR_Z + 1.5))
    for y in (-TRAY_W / 2 + 1.5, TRAY_W / 2 - 1.5):
        place("Tray_Long_Lip", "Tray", PARTS["Tray_Long_Lip_600x40x3"], (0, y, TRAY_FLOOR_Z + 3 + TRAY_LIP_H / 2))
    for x in (-TRAY_L / 2 + 1.5, TRAY_L / 2 - 1.5):
        place(
            "Tray_Short_Lip",
            "Tray",
            PARTS["Tray_Short_Lip_400x40x3"].rotate((0, 0, 0), (0, 0, 1), 90),
            (x, 0, TRAY_FLOOR_Z + 3 + TRAY_LIP_H / 2),
        )
    place("Tray_NonSlip_Mat", "Tray", PARTS["Tray_NonSlip_Mat_580x380x2"], (0, 0, TRAY_FLOOR_Z + 4.0))

    # Loader pivot structure and a floor-pickup pose.
    for y in (-100.0, 100.0):
        place("Loader_Pivot_Gusset", "Loader", PARTS["Loader_Pivot_Gusset"], (160.0, y, 190.0))
        add_y_axis_part("Loader_Pivot_Bearing", "Loader", "Loader_Pivot_Bearing_Envelope", (160.0, y, 190.0))
    add_y_axis_part("Loader_Pivot_Cross_Shaft", "Loader", "Loader_Pivot_Cross_Shaft_D20", LOADER_PIVOT)
    arm = PARTS["Loader_Arm_25x20x600"]
    theta = LOADER_PICKUP_DEG
    for y in (-100.0, 100.0):
        arm_world = arm.rotate((0, 0, 0), (0, 1, 0), -theta).translate(
            v(LOADER_PIVOT[0], y, LOADER_PIVOT[2])
        )
        place("Loader_Arm", "Loader", arm_world, (0, 0, 0))
    tip_x = LOADER_PIVOT[0] + LOADER_ARM_L * math.cos(math.radians(theta))
    tip_z = LOADER_PIVOT[2] + LOADER_ARM_L * math.sin(math.radians(theta))
    place("Loader_Tip_Crossbar", "Loader", PARTS["Loader_Tip_Crossbar"], (tip_x, 0, tip_z))

    # Cable sectors and a dual-groove winch concept.
    for y in (-130.0, 130.0):
        add_y_axis_part("Cable_Sector", "Winch", "Cable_Sector_R150", (160.0, y, 190.0))
    add_y_axis_part("Winch_Drum", "Winch", "Winch_Drum_D50_W60", (-250.0, 0.0, 150.0))
    for y in (-34.0, 34.0):
        add_y_axis_part("Winch_Drum_Flange", "Winch", "Winch_Drum_Flange_D90", (-250.0, y, 150.0))
    add_y_axis_part("Winch_Ratchet_Disc", "Winch", "Winch_Ratchet_Disc_D90", (-250.0, -43.0, 150.0))
    place("Winch_Pawl", "Winch", PARTS["Winch_Pawl"], (-207.0, -43.0, 190.0))
    add_y_axis_part("Winch_Motor", "Winch", "Winch_Motor_24V_25Nm_Envelope", (-315.0, -100.0, 150.0))
    for y in (-105.0, 105.0):
        add_y_axis_part("Cable_Guide_Sheave", "Winch", "Cable_Guide_Sheave_D60", (80.0, y, 420.0))
        place("Cable_LoadCell", "Shovel", PARTS["Cable_LoadCell_1kN_Envelope"], (60.0, y, 385.0))
    # Cable as two straight concept runs to the pivot sectors; final routing needs motion checks.
    for y in (-105.0, 105.0):
        cable = cylinder_between((-250.0, y, 150.0), (160.0, y, 340.0), 2.0)
        place("Lift_Cable_Concept_Run", "Winch", cable, (0, 0, 0))

    # Bucket and tilt actuator in the nominal pickup pose.
    bucket_angle = 0.0
    bucket_world = PARTS["Shovel_Bucket_300x180"].rotate(
        (0, 0, 0), (0, 1, 0), -bucket_angle
    ).translate(v(tip_x, 0, tip_z))
    place("Shovel_Bucket", "Shovel", bucket_world, (0, 0, 0))
    for y in (-155.0, 155.0):
        place("Shovel_Hinge_Cheek", "Shovel", PARTS["Shovel_Hinge_Cheek"], (tip_x, y, tip_z))
    # Actuator endpoints are tied to the arm (r=180 mm) and bucket (x=-120 mm).
    a = (
        LOADER_PIVOT[0] + 180 * math.cos(math.radians(theta)),
        0.0,
        LOADER_PIVOT[2] + 180 * math.sin(math.radians(theta)),
    )
    b_nominal = (tip_x - 120.0, 0.0, tip_z)
    delta = tuple(b_nominal[i] - a[i] for i in range(3))
    actuator_length = math.sqrt(sum(component * component for component in delta))
    actuator_direction = tuple(component / actuator_length for component in delta)
    # The envelope has a 315 mm eye-to-eye retracted length and 150 mm stroke.
    b = tuple(a[i] + actuator_direction[i] * 315.0 for i in range(3))
    actuator = align_local_z(
        PARTS["Linear_Actuator_24V_150mm_Envelope"], a, b, local_start_z=-90.0
    )
    place("Bucket_Tilt_Actuator", "Shovel", actuator, (0, 0, 0))
    bracket = PARTS["Shovel_Actuator_Bracket"]
    place(
        "Bucket_Tilt_Actuator_Arm_Bracket",
        "Shovel",
        align_local_z(bracket, a, b),
        (0, 0, 0),
    )
    place(
        "Bucket_Tilt_Actuator_Bucket_Bracket",
        "Shovel",
        align_local_z(bracket, b, a),
        (0, 0, 0),
    )
    for y in (-55.0, 55.0):
        place("Obstacle_Sensor", "Sensors", PARTS["Obstacle_Sensor_Envelope"], (390.0, y, 150.0))
    place("Line_Sensor_Array", "Sensors", PARTS["Line_Sensor_Array_100x14"], (350.0, 0.0, 9.0))
    place("HMI_Display", "Sensors", PARTS["HMI_Display_Envelope"], (405.0, 0.0, 340.0))
    place("Emergency_Stop", "Sensors", PARTS["Emergency_Stop_Envelope"], (415.0, -80.0, 300.0))
    place("Object_Camera", "Sensors", PARTS["Object_Camera_Envelope"], (405.0, 0.0, 760.0))
    place("Phone_Mount_Arm", "Sensors", PARTS["Phone_Mount_Arm"], (385.0, 0.0, 850.0))
    place("Phone_Clamp", "Sensors", PARTS["Phone_Clamp_Assembly"], (408.0, 0.0, 925.0))
    for x in (-380.0, 380.0):
        for y in (-205.0, 205.0):
            place("Sensor_Bumper_Bracket", "Sensors", PARTS["Sensor_Bumper_Bracket"], (x, y, 115.0))


def export_parts() -> None:
    for name, shape in PARTS.items():
        subsystem = PART_META[name].subsystem
        folder = STEP_ROOT / "Parts" / subsystem
        folder.mkdir(parents=True, exist_ok=True)
        cq.exporters.export(shape, str(folder / f"{name}.step"), exportType="STEP")


def export_assemblies() -> None:
    assembly_folder = STEP_ROOT / "Assemblies"
    assembly_folder.mkdir(parents=True, exist_ok=True)
    colors = {
        "Chassis": cq.Color(0.55, 0.60, 0.64),
        "Mobility": cq.Color(0.15, 0.19, 0.22),
        "GearTrain": cq.Color(0.82, 0.61, 0.24),
        "Power": cq.Color(0.18, 0.35, 0.65),
        "Sensors": cq.Color(0.1, 0.65, 0.68),
        "Loader": cq.Color(0.88, 0.48, 0.16),
        "Winch": cq.Color(0.62, 0.65, 0.68),
        "Shovel": cq.Color(0.78, 0.80, 0.82),
        "Tray": cq.Color(0.40, 0.62, 0.40),
    }
    overall = cq.Assembly(name="ROBOT_V1_PRELIMINARY")
    for shape, name, subsystem in INSTANCES:
        overall.add(shape, name=name, color=colors.get(subsystem))
    overall.save(
        str(assembly_folder / "RobotV1_Overall_Assembly.step"),
        exportType="STEP",
        tolerance=0.05,
        angularTolerance=0.08,
    )
    for subsystem, items in SUBSYSTEM_INSTANCES.items():
        assembly = cq.Assembly(name=f"RobotV1_{subsystem}")
        for shape, name in items:
            assembly.add(shape, name=name)
        target = assembly_folder / f"RobotV1_{subsystem}_Assembly.step"
        assembly.save(str(target), exportType="STEP", tolerance=0.05, angularTolerance=0.08)

    # Exploded STEP: subsystem groups are displaced only for communication, not assembly.
    offsets = {
        "Chassis": (0, 0, 0),
        "Mobility": (0, 0, -130),
        "GearTrain": (0, 0, 90),
        "Power": (0, 0, 110),
        "Sensors": (0, 0, 170),
        "Loader": (80, 0, 220),
        "Winch": (-80, 0, 130),
        "Shovel": (180, 0, 220),
        "Tray": (0, 0, 260),
    }
    exploded = cq.Assembly(name="RobotV1_Exploded_Concept")
    for shape, name, subsystem in INSTANCES:
        dx, dy, dz = offsets[subsystem]
        exploded.add(shape.translate(v(dx, dy, dz)), name=name)
    exploded.save(
        str(assembly_folder / "RobotV1_Exploded_Concept.step"),
        exportType="STEP",
        tolerance=0.05,
        angularTolerance=0.08,
    )


def write_bom() -> None:
    out = FOLDERS["calcs"] / "RobotV1_BOM_Preliminary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Item", "Part / Envelope", "Qty", "Subsystem", "Material / Source", "Status", "Notes"])
        for index, (name, meta) in enumerate(sorted(PART_META.items()), 1):
            qty = COUNTS.get(name, 0)
            writer.writerow([index, name, qty, meta.subsystem, meta.material, meta.status, meta.note])


def new_dxf():
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    doc.header["$INSUNITS"] = ezdxf.units.MM
    doc.header["$MEASUREMENT"] = 1
    for layer, color in [
        ("OUTLINE", 7),
        ("CENTER", 4),
        ("HIDDEN", 8),
        ("DIMENSION", 2),
        ("TEXT", 3),
        ("REFERENCE", 5),
    ]:
        doc.layers.new(layer, dxfattribs={"color": color})
    return doc, doc.modelspace()


def add_rect(msp, x: float, y: float, w: float, h: float, layer: str = "OUTLINE"):
    msp.add_lwpolyline(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
        close=True,
        dxfattribs={"layer": layer},
    )


def add_text(msp, x: float, y: float, text: str, height: float = 4.0):
    msp.add_text(text, dxfattribs={"height": height, "layer": "TEXT"}).set_placement((x, y))


def add_dim(msp, x1, y1, x2, y2, label: str, tx, ty):
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "DIMENSION"})
    add_text(msp, tx, ty, label, 3.5)


def export_drawings() -> None:
    drawings = FOLDERS["drawings"]
    drawings.mkdir(parents=True, exist_ok=True)

    # Overall plan, side and front elevation reference views.
    doc, msp = new_dxf()
    add_text(msp, -400, 265, "ROBOT V1 - TOP / PLAN (mm), PRELIMINARY")
    add_rect(msp, -FRAME_L / 2, -FRAME_W / 2, FRAME_L, FRAME_W)
    add_rect(msp, -TRAY_L / 2, -TRAY_W / 2, TRAY_L, TRAY_W, "HIDDEN")
    for x in (-WHEEL_X, WHEEL_X):
        for y in (-WHEEL_Y, WHEEL_Y):
            radius = WHEEL_D / 2 if (x > 0 and y < 0) or (x < 0 and y > 0) else CASTER_D / 2
            msp.add_circle((x, y), radius, dxfattribs={"layer": "OUTLINE"})
            msp.add_circle((x, y), 8, dxfattribs={"layer": "CENTER"})
    add_rect(msp, -360, -135, 720, 270, "HIDDEN")
    add_rect(msp, -TRAY_L / 2, -TRAY_W / 2, TRAY_L, TRAY_W, "REFERENCE")
    # Loader working envelope and its pivot-to-tip ray in pickup pose.
    tip_x = LOADER_PIVOT[0] + LOADER_ARM_L * math.cos(math.radians(LOADER_PICKUP_DEG))
    tip_z = LOADER_PIVOT[2] + LOADER_ARM_L * math.sin(math.radians(LOADER_PICKUP_DEG))
    msp.add_line(LOADER_PIVOT[:2], (tip_x, 0), dxfattribs={"layer": "REFERENCE"})
    msp.add_circle((LOADER_PIVOT[0], 0), 18, dxfattribs={"layer": "CENTER"})
    add_dim(msp, -400, -260, 400, -260, "FRAME 800", -80, -250)
    add_dim(msp, 430, -225, 430, 225, "FRAME WIDTH 450", 440, 0)
    add_text(msp, -390, -295, "WHEELBASE 640 / TRACK 380 / DIAGONAL DRIVE + PASSIVE CASTER PAIR")

    # Side elevation at a separate drawing origin.
    ox, oy = 1100.0, 0.0
    add_text(msp, ox - 420, oy + 1030, "ROBOT V1 - SIDE ELEVATION (mm), PICKUP POSE")
    add_rect(msp, ox - 400, oy + 30, 800, 33)
    add_rect(msp, ox - 360, oy + 65, 720, 190)
    for x in (-320, 320):
        rad = 75 if x > 0 else 45
        msp.add_circle((ox + x, oy + rad), rad, dxfattribs={"layer": "OUTLINE"})
    add_rect(msp, ox - 300, oy + TRAY_FLOOR_Z, 600, TRAY_LIP_H + 3)
    for x in (-260, 260):
        add_rect(msp, ox + x - 10, oy + 260, 20, 480)
    pivot_x, pivot_z = LOADER_PIVOT[0], LOADER_PIVOT[2]
    arm_tip_x, arm_tip_z = tip_x, tip_z
    msp.add_line((ox + pivot_x, oy + pivot_z), (ox + arm_tip_x, oy + arm_tip_z), dxfattribs={"layer": "OUTLINE"})
    # Raised pose overlay.
    tray_tip_x = LOADER_PIVOT[0] + LOADER_ARM_L * math.cos(math.radians(LOADER_TRAY_DEG))
    tray_tip_z = LOADER_PIVOT[2] + LOADER_ARM_L * math.sin(math.radians(LOADER_TRAY_DEG))
    msp.add_line((ox + pivot_x, oy + pivot_z), (ox + tray_tip_x, oy + tray_tip_z), dxfattribs={"layer": "REFERENCE"})
    msp.add_text("PICKUP", dxfattribs={"height": 5, "layer": "TEXT"}).set_placement((ox + arm_tip_x - 50, oy + arm_tip_z - 20))
    msp.add_text("TRAY POSITION", dxfattribs={"height": 5, "layer": "TEXT"}).set_placement((ox + tray_tip_x + 10, oy + tray_tip_z))
    add_dim(msp, ox - 400, oy - 35, ox + 400, oy - 35, "CHASSIS 800", ox - 80, oy - 27)
    add_dim(msp, ox + 440, oy, ox + 440, oy + 783, "TRAY TOP 783", ox + 450, oy + 380)
    add_text(msp, ox - 390, oy + 300, "ENCLOSURE ENVELOPE 720 x 270 x 190")
    add_text(msp, ox - 390, oy + 25, "GROUND CLEARANCE 30 TARGET")

    # Front elevation at another drawing origin.
    fx, fy = 1100.0, 1200.0
    add_text(msp, fx - 240, fy + 1030, "ROBOT V1 - FRONT ELEVATION (mm)")
    add_rect(msp, fx - 225, fy + 30, 450, 33)
    add_rect(msp, fx - 135, fy + 65, 270, 190)
    for y in (-190, 190):
        msp.add_circle((fx + y, fy + 75), 75, dxfattribs={"layer": "OUTLINE"})
    add_rect(msp, fx - 200, fy + TRAY_FLOOR_Z, 400, TRAY_LIP_H + 3)
    for y in (-175, 175):
        add_rect(msp, fx + y - 10, fy + 260, 20, 480)
    add_dim(msp, fx - 225, fy - 35, fx + 225, fy - 35, "FRAME WIDTH 450", fx - 65, fy - 25)
    add_dim(msp, fx - 190, fy - 70, fx + 190, fy - 70, "DRIVE TRACK 380", fx - 65, fy - 60)
    add_text(msp, fx - 200, fy + 780, "TRAY 600 x 400; 40 mm LIPS")
    doc.saveas(drawings / "RobotV1_Overall_Orthographic_Layout.dxf")

    # Gear train detail with pitch circles and exact nominal center distances.
    doc, msp = new_dxf()
    add_text(msp, -10, 130, "THREE-GEAR DRIVE REDUCTION - SIDE VIEW, mm")
    for teeth, cx in zip(GEAR_TEETH, GEAR_CENTER_X):
        pitch_r = teeth * GEAR_MODULE / 2
        outside_r = (teeth + 2) * GEAR_MODULE / 2
        root_r = (teeth - 2.5) * GEAR_MODULE / 2
        msp.add_circle((cx, 0), outside_r, dxfattribs={"layer": "OUTLINE"})
        msp.add_circle((cx, 0), pitch_r, dxfattribs={"layer": "REFERENCE"})
        msp.add_circle((cx, 0), root_r, dxfattribs={"layer": "HIDDEN"})
        add_text(msp, cx - 15, -outside_r - 15, f"{teeth}T / M2")
    add_dim(msp, 0, -125, 54, -125, "C1-C2 = 54", 7, -118)
    add_dim(msp, 54, -145, 126, -145, "C2-C3 = 72", 64, -138)
    add_text(msp, -10, 145, "20 DEG PRESSURE ANGLE / FACE 20 / OVERALL REDUCTION 3:1")
    add_text(msp, -10, -190, "OUTSIDE DIAMETERS 40 / 76 / 112; TOOTH PROFILE REQUIRES SUPPLIER VALIDATION")
    doc.saveas(drawings / "Drive_Three_Gear_Train_Detail.dxf")

    # Chassis underside drawing.
    doc, msp = new_dxf()
    add_text(msp, -420, 265, "CHASSIS FRAME + UNDERSIDE - PRELIMINARY")
    add_rect(msp, -400, -225, 800, 450)
    for y in (-110, 110):
        add_rect(msp, -400, y - 15, 800, 30)
    for x in (-220, 0, 220):
        add_rect(msp, x - 15, -225, 30, 450)
    for x in (-320, 320):
        for y in (-190, 190):
            radius = 75 if (x > 0 and y < 0) or (x < 0 and y > 0) else 45
            msp.add_circle((x, y), radius, dxfattribs={"layer": "REFERENCE"})
    add_text(msp, -390, -260, "30x30x2 mm EXTRUSION RAILS; 3 mm DECK; CROSSMEMBERS AT 250 mm NOMINAL")
    add_text(msp, -390, -280, "POWERED: FRONT LEFT + REAR RIGHT; PASSIVE CASTER: FRONT RIGHT + REAR LEFT")
    doc.saveas(drawings / "Chassis_Underside_and_Wheel_Layout.dxf")

    # Loader side positions and cable sector.
    doc, msp = new_dxf()
    add_text(msp, -50, 900, "LOADER MOTION REFERENCE - SIDE VIEW (mm)")
    msp.add_circle((LOADER_PIVOT[0], LOADER_PIVOT[2]), 150, dxfattribs={"layer": "REFERENCE"})
    for angle, layer, label in [
        (LOADER_PICKUP_DEG, "OUTLINE", "PICKUP -15 DEG"),
        (LOADER_TRAY_DEG, "REFERENCE", "TRAY +75 DEG"),
    ]:
        tx = LOADER_PIVOT[0] + LOADER_ARM_L * math.cos(math.radians(angle))
        tz = LOADER_PIVOT[2] + LOADER_ARM_L * math.sin(math.radians(angle))
        msp.add_line(LOADER_PIVOT[:2], (tx, tz), dxfattribs={"layer": layer})
        msp.add_circle((tx, tz), 8, dxfattribs={"layer": layer})
        add_text(msp, tx + 8, tz, label)
    msp.add_circle((LOADER_PIVOT[0], LOADER_PIVOT[2]), 20, dxfattribs={"layer": "OUTLINE"})
    add_text(msp, -40, 820, "DUAL CABLES ON R150 SECTORS; WINCH WITH INDEPENDENT BRAKE/PAWL REQUIRED")
    add_text(msp, -40, 790, "ARM LENGTH 600 / SHOVEL WIDTH 300 / SHOVEL DEPTH 180")
    add_text(msp, -40, 760, "POSES ARE ENVELOPE CHECKS; LINKAGE, CABLE ANGLES, STOPS, AND INTERFERENCE NEED PROTOTYPE CHECKS")
    doc.saveas(drawings / "Loader_Pickup_and_Tray_Positions.dxf")


def validate_and_report() -> list[str]:
    report = []
    for name, shape in PARTS.items():
        if not shape.isValid():
            raise RuntimeError(f"{name} is not a valid B-rep.")
        count = len(shape.Solids())
        if count < 1:
            raise RuntimeError(f"{name} contains no solid.")
        bb = shape.BoundingBox()
        report.append(
            f"{name}: {count} solid(s), {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm, "
            f"volume {shape.Volume():.1f} mm^3"
        )
    return report


def main() -> None:
    build_parts()
    build_assembly_instances()
    validate_and_report()
    export_parts()
    export_assemblies()
    print(f"Unique parts: {len(PARTS)}")
    print(f"Placed instances: {len(INSTANCES)}")
    print(f"STEP-only CAD package: {STEP_ROOT}")


if __name__ == "__main__":
    main()
