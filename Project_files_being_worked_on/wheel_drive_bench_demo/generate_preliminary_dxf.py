"""Create a simple, editable DXF envelope drawing from the concept JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable


PROJECT_DIR = Path(__file__).resolve().parent
PILOT_DIR = PROJECT_DIR.parent / "fusion_native_pilot"
if str(PILOT_DIR) not in sys.path:
    sys.path.insert(0, str(PILOT_DIR))

from fusion_model_spec import validate_model_spec


class DxfWriter:
    def __init__(self) -> None:
        self.entities: list[str] = []

    @staticmethod
    def _value(value: float) -> str:
        return f"{float(value):.6f}".rstrip("0").rstrip(".") or "0"

    def _entity(self, kind: str, values: Iterable[tuple[int, str]]) -> None:
        self.entities.extend(("0", kind))
        for code, value in values:
            self.entities.extend((str(code), value))

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        layer: str = "OUTLINE",
    ) -> None:
        self._entity(
            "LINE",
            (
                (8, layer),
                (10, self._value(x1)),
                (20, self._value(y1)),
                (30, "0"),
                (11, self._value(x2)),
                (21, self._value(y2)),
                (31, "0"),
            ),
        )

    def circle(
        self, x: float, y: float, radius: float, layer: str = "OUTLINE"
    ) -> None:
        self._entity(
            "CIRCLE",
            (
                (8, layer),
                (10, self._value(x)),
                (20, self._value(y)),
                (30, "0"),
                (40, self._value(radius)),
            ),
        )

    def text(
        self,
        x: float,
        y: float,
        value: str,
        height: float = 2.5,
        layer: str = "TEXT",
    ) -> None:
        safe_value = value.encode("ascii", "replace").decode("ascii")
        self._entity(
            "TEXT",
            (
                (8, layer),
                (10, self._value(x)),
                (20, self._value(y)),
                (30, "0"),
                (40, self._value(height)),
                (1, safe_value),
            ),
        )

    def rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        layer: str = "OUTLINE",
    ) -> None:
        self.line(x, y, x + width, y, layer)
        self.line(x + width, y, x + width, y + height, layer)
        self.line(x + width, y + height, x, y + height, layer)
        self.line(x, y + height, x, y, layer)

    def horizontal_dimension(
        self,
        x1: float,
        x2: float,
        object_y: float,
        dimension_y: float,
        label: str,
    ) -> None:
        size = 1.5
        self.line(x1, object_y, x1, dimension_y - 1, "DIMENSIONS")
        self.line(x2, object_y, x2, dimension_y - 1, "DIMENSIONS")
        self.line(x1, dimension_y, x2, dimension_y, "DIMENSIONS")
        self.line(x1, dimension_y, x1 + size, dimension_y + size / 2, "DIMENSIONS")
        self.line(x1, dimension_y, x1 + size, dimension_y - size / 2, "DIMENSIONS")
        self.line(x2, dimension_y, x2 - size, dimension_y + size / 2, "DIMENSIONS")
        self.line(x2, dimension_y, x2 - size, dimension_y - size / 2, "DIMENSIONS")
        text_x = (x1 + x2) / 2 - len(label) * 0.7
        self.text(text_x, dimension_y + 1.5, label, 2.0, "DIMENSIONS")

    def vertical_dimension(
        self,
        y1: float,
        y2: float,
        object_x: float,
        dimension_x: float,
        label: str,
    ) -> None:
        size = 1.5
        self.line(object_x, y1, dimension_x + 1, y1, "DIMENSIONS")
        self.line(object_x, y2, dimension_x + 1, y2, "DIMENSIONS")
        self.line(dimension_x, y1, dimension_x, y2, "DIMENSIONS")
        self.line(dimension_x, y1, dimension_x + size / 2, y1 + size, "DIMENSIONS")
        self.line(dimension_x, y1, dimension_x - size / 2, y1 + size, "DIMENSIONS")
        self.line(dimension_x, y2, dimension_x + size / 2, y2 - size, "DIMENSIONS")
        self.line(dimension_x, y2, dimension_x - size / 2, y2 - size, "DIMENSIONS")
        self.text(dimension_x + 2, (y1 + y2) / 2, label, 2.0, "DIMENSIONS")

    def panel(self, x: float, y: float, title: str, note: str) -> None:
        self.rectangle(x, y, 196, 144, "FRAME")
        self.text(x + 5, y + 136, title, 3.0)
        self.text(x + 5, y + 128, note, 2.0)

    def render(self) -> str:
        lines = [
            "0",
            "SECTION",
            "2",
            "HEADER",
            "9",
            "$ACADVER",
            "1",
            "AC1015",
            "9",
            "$INSUNITS",
            "70",
            "4",
            "9",
            "$MEASUREMENT",
            "70",
            "1",
            "0",
            "ENDSEC",
            "0",
            "SECTION",
            "2",
            "TABLES",
            "0",
            "TABLE",
            "2",
            "LTYPE",
            "70",
            "1",
            "0",
            "LTYPE",
            "2",
            "CONTINUOUS",
            "70",
            "0",
            "3",
            "Solid line",
            "72",
            "65",
            "73",
            "0",
            "40",
            "0",
            "0",
            "ENDTAB",
            "0",
            "TABLE",
            "2",
            "LAYER",
            "70",
            "5",
        ]
        for name, color in (
            ("0", 7),
            ("OUTLINE", 7),
            ("DIMENSIONS", 2),
            ("TEXT", 3),
            ("FRAME", 8),
        ):
            lines.extend(
                (
                    "0",
                    "LAYER",
                    "2",
                    name,
                    "70",
                    "0",
                    "62",
                    str(color),
                    "6",
                    "CONTINUOUS",
                )
            )
        lines.extend(("0", "ENDTAB", "0", "ENDSEC", "0", "SECTION", "2", "ENTITIES"))
        lines.extend(self.entities)
        lines.extend(("0", "ENDSEC", "0", "EOF"))
        return "\n".join(lines) + "\n"


def _components_by_name(spec: dict) -> dict[str, dict]:
    return {component["name"]: component for component in spec["components"]}


def _add_wheel(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    outer = dims["outer_diameter"]
    bore = dims["inner_diameter"]
    width = dims["height"]
    cx, cy = x + 55, y + 76
    writer.circle(cx, cy, outer / 2)
    writer.circle(cx, cy, bore / 2)
    writer.text(x + 40, y + 28, "END VIEW", 2.0)
    writer.vertical_dimension(
        cy - outer / 2, cy + outer / 2, cx + outer / 2, x + 104, f"DIA {outer:g}"
    )

    sx, sy = x + 128, cy - outer / 2
    writer.rectangle(sx, sy, width, outer)
    writer.text(sx + 2, y + 28, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + width, sy, sy - 8, f"{width:g}")
    writer.text(x + 16, y + 12, f"BORE DIA {bore:g}", 2.2)


def _add_hub(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    outer = dims["outer_diameter"]
    bore = dims["inner_diameter"]
    width = dims["height"]
    cx, cy = x + 55, y + 76
    writer.circle(cx, cy, outer / 2)
    writer.circle(cx, cy, bore / 2)
    writer.text(x + 40, y + 50, "END VIEW", 2.0)
    writer.vertical_dimension(
        cy - outer / 2, cy + outer / 2, cx + outer / 2, x + 82, f"DIA {outer:g}"
    )
    sx, sy = x + 128, cy - outer / 2
    writer.rectangle(sx, sy, width, outer)
    writer.text(sx, y + 50, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + width, sy, sy - 8, f"{width:g}")
    writer.text(x + 16, y + 36, f"BORE DIA {bore:g}", 2.2)


def _add_shaft(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    diameter = dims["diameter"]
    length = dims["height"]
    cx, cy = x + 55, y + 76
    writer.circle(cx, cy, diameter / 2)
    writer.text(x + 42, y + 62, "END VIEW", 2.0)
    sx, sy = x + 97, cy - diameter / 2
    writer.rectangle(sx, sy, length, diameter)
    writer.text(sx + 10, y + 62, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + length, sy, sy - 8, f"{length:g}")
    writer.vertical_dimension(
        sy, sy + diameter, sx + length, sx + length + 5, f"DIA {diameter:g}"
    )


def _add_bearing(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    outer = dims["outer_diameter"]
    inner = dims["inner_diameter"]
    width = dims["height"]
    cx, cy = x + 55, y + 76
    writer.circle(cx, cy, outer / 2)
    writer.circle(cx, cy, inner / 2)
    writer.text(x + 40, y + 56, "END VIEW", 2.0)
    sx, sy = x + 128, cy - outer / 2
    writer.rectangle(sx, sy, width, outer)
    writer.text(sx - 1, y + 56, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + width, sy, sy - 8, f"{width:g}")
    writer.text(x + 20, y + 38, f"OD {outer:g} / ID {inner:g}", 2.2)


def _add_support(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    length = dims["length"]
    width = dims["width"]
    thickness = dims["height"]
    bore = dims["bore_diameter"]
    left, bottom = x + 40, y + 62
    cx, cy = left + length / 2, bottom + width / 2
    writer.rectangle(left, bottom, length, width)
    writer.circle(cx, cy, bore / 2)
    writer.text(x + 40, y + 50, "END VIEW", 2.0)
    writer.horizontal_dimension(left, left + length, bottom, bottom - 8, f"{length:g}")
    writer.vertical_dimension(
        bottom, bottom + width, left + length, left + length + 6, f"{width:g}"
    )
    sx, sy = x + 130, bottom
    writer.rectangle(sx, sy, thickness, width)
    writer.text(sx, y + 50, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + thickness, sy, sy - 8, f"{thickness:g}")
    writer.text(x + 20, y + 38, f"CENTER BORE DIA {bore:g}", 2.2)


def _add_coupling(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    diameter = dims["diameter"]
    length = dims["height"]
    cx, cy = x + 55, y + 76
    writer.circle(cx, cy, diameter / 2)
    writer.text(x + 41, y + 62, "END VIEW", 2.0)
    sx, sy = x + 128, cy - diameter / 2
    writer.rectangle(sx, sy, length, diameter)
    writer.text(sx - 1, y + 62, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(sx, sx + length, sy, sy - 8, f"{length:g}")
    writer.text(x + 18, y + 42, f"ENVELOPE DIA {diameter:g}; BORES UNSPECIFIED", 2.0)


def _add_motor(writer: DxfWriter, x: float, y: float, part: dict) -> None:
    dims = part["dimensions_mm"]
    length = dims["length"]
    width = dims["width"]
    axis_length = dims["height"]

    end_x, end_y = x + 44, y + 68
    writer.rectangle(end_x, end_y, length, width)
    writer.text(x + 45, y + 56, "END VIEW", 2.0)
    writer.text(x + 12, y + 40, f"{length:g} X {width:g} END ENVELOPE", 2.1)

    side_x, side_y = x + 126, y + 68
    writer.rectangle(side_x, side_y, axis_length, width)
    writer.text(side_x + 3, y + 56, "SIDE VIEW", 2.0)
    writer.horizontal_dimension(
        side_x, side_x + axis_length, side_y, side_y - 8, f"{axis_length:g}"
    )
    writer.text(x + 20, y + 30, "FF-130 CANDIDATE BODY ENVELOPE ONLY", 2.0)


def build_dxf(spec: dict) -> str:
    parts = _components_by_name(spec)
    required_names = (
        "Wheel Rim Placeholder",
        "Wheel Hub Placeholder",
        "Drive Shaft Placeholder",
        "Bearing Envelope Placeholder",
        "Bearing Support Plate Placeholder",
        "Coupling Envelope Placeholder",
        "FF-130 Motor Candidate Envelope",
    )
    missing = [name for name in required_names if name not in parts]
    if missing:
        raise ValueError(f"Concept specification is missing parts: {', '.join(missing)}")

    writer = DxfWriter()
    writer.text(8, 468, "WHEEL DRIVE BENCH DEMONSTRATOR - PRELIMINARY A0", 5.0)
    writer.text(
        8,
        458,
        "UNITS: MM | 1:1 ENVELOPES | PLACEHOLDERS ONLY | NOT FOR MANUFACTURE",
        2.8,
    )
    panel_items = (
        ("Wheel rim", "PLACEHOLDER - VERIFY WHEEL INTERFACES", _add_wheel, parts[required_names[0]]),
        ("Wheel hub", "PLACEHOLDER - VERIFY SHAFT BORE AND RETENTION", _add_hub, parts[required_names[1]]),
        ("Drive shaft", "ASSUMED DIAMETER AND LENGTH", _add_shaft, parts[required_names[2]]),
        ("Bearing envelope", "NO BEARING PART NUMBER OR FIT SELECTED", _add_bearing, parts[required_names[3]]),
        ("Bearing support plate", "NO MOUNTING HOLES OR FASTENERS DEFINED", _add_support, parts[required_names[4]]),
        ("Coupling envelope", "MOTOR-SHAFT BORE NOT MODELED", _add_coupling, parts[required_names[5]]),
        ("Motor body envelope", "CANDIDATE ONLY - SHAFT INTERFACE UNKNOWN", _add_motor, parts[required_names[6]]),
    )
    for index, (title, note, draw_part, part) in enumerate(panel_items):
        column = index % 3
        row = index // 3
        x = column * 200
        y = (2 - row) * 150
        writer.panel(x, y, title, note)
        draw_part(writer, x, y, part)

    writer.text(
        8,
        4,
        "NO TOLERANCES, FITS, MATERIALS, OR MANUFACTURING PROCESS SPECIFIED.",
        2.3,
        "TEXT",
    )
    return writer.render()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        type=Path,
        default=PROJECT_DIR / "preliminary_wheel_drive_spec.json",
        help="Validated wheel-drive model specification.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_DIR / "wheel_drive_parts_A0.dxf",
        help="Output DXF path.",
    )
    args = parser.parse_args()

    spec = validate_model_spec(json.loads(args.spec.read_text(encoding="utf-8")))
    dxf_text = build_dxf(spec)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dxf_text, encoding="ascii", newline="\n")
    print(f"Wrote preliminary drawing: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
