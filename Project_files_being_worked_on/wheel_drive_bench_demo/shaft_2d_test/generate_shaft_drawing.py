"""Generate a preliminary, editable DXF detail for the wheel-drive shaft."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote


HERE = Path(__file__).resolve().parent
PROJECT_DIR = HERE.parent
PILOT_DIR = PROJECT_DIR.parent / "fusion_native_pilot"

sys.path.insert(0, str(PILOT_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from fusion_model_spec import validate_model_spec
from generate_preliminary_dxf import DxfWriter


SHEET_WIDTH_MM = 297
SHEET_HEIGHT_MM = 210


class ShaftDrawing:
    """Keep the DXF and its visual preview generated from the same geometry."""

    def __init__(self) -> None:
        self.dxf = DxfWriter()
        self.svg: list[str] = []

    @staticmethod
    def _svg_y(y: float) -> float:
        return SHEET_HEIGHT_MM - y

    @staticmethod
    def _svg_class(layer: str) -> str:
        return {
            "OUTLINE": "outline",
            "DIMENSIONS": "dimension",
            "TEXT": "drawing-text",
            "FRAME": "frame",
        }.get(layer, "outline")

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        layer: str = "OUTLINE",
    ) -> None:
        self.dxf.line(x1, y1, x2, y2, layer)
        self.svg.append(
            f'<line class="{self._svg_class(layer)}" x1="{x1:g}" '
            f'y1="{self._svg_y(y1):g}" x2="{x2:g}" y2="{self._svg_y(y2):g}"/>'
        )

    def circle(
        self, x: float, y: float, radius: float, layer: str = "OUTLINE"
    ) -> None:
        self.dxf.circle(x, y, radius, layer)
        self.svg.append(
            f'<circle class="{self._svg_class(layer)}" cx="{x:g}" '
            f'cy="{self._svg_y(y):g}" r="{radius:g}"/>'
        )

    def text(
        self,
        x: float,
        y: float,
        value: str,
        height: float = 2.0,
        layer: str = "TEXT",
    ) -> None:
        self.dxf.text(x, y, value, height, layer)
        self.svg.append(
            f'<text class="{self._svg_class(layer)}" x="{x:g}" '
            f'y="{self._svg_y(y):g}" font-size="{height:g}">'
            f"{html.escape(value)}</text>"
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
        arrow = 1.5
        self.line(x1, object_y, x1, dimension_y - 1, "DIMENSIONS")
        self.line(x2, object_y, x2, dimension_y - 1, "DIMENSIONS")
        self.line(x1, dimension_y, x2, dimension_y, "DIMENSIONS")
        self.line(
            x1, dimension_y, x1 + arrow, dimension_y + arrow / 2, "DIMENSIONS"
        )
        self.line(
            x1, dimension_y, x1 + arrow, dimension_y - arrow / 2, "DIMENSIONS"
        )
        self.line(
            x2, dimension_y, x2 - arrow, dimension_y + arrow / 2, "DIMENSIONS"
        )
        self.line(
            x2, dimension_y, x2 - arrow, dimension_y - arrow / 2, "DIMENSIONS"
        )
        self.text(
            (x1 + x2) / 2 - len(label) * 0.7,
            dimension_y + 1.5,
            label,
            2.0,
            "DIMENSIONS",
        )

    def render_svg(self) -> str:
        return f"""<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 {SHEET_WIDTH_MM} {SHEET_HEIGHT_MM}"
  role="img" aria-labelledby="title description">
  <title id="title">Preliminary shaft drawing, 6 mm diameter by 46 mm long</title>
  <desc id="description">A 1:1 millimetre drawing with a side view, end view,
    length and diameter annotations. All dimensions are provisional.</desc>
  <style>
    .outline {{ fill: none; stroke: #18212b; stroke-width: 0.35; }}
    .dimension {{ fill: none; stroke: #2866a6; stroke-width: 0.22; }}
    .frame {{ fill: none; stroke: #77818c; stroke-width: 0.22; }}
    .drawing-text {{ fill: #18212b; stroke: none; font-family: Arial, sans-serif; }}
    text.dimension {{ fill: #2866a6; stroke: none; font-family: Arial, sans-serif; }}
  </style>
  <rect x="0" y="0" width="{SHEET_WIDTH_MM}" height="{SHEET_HEIGHT_MM}" fill="#fff"/>
  {''.join(self.svg)}
</svg>"""


def load_shaft_dimensions() -> tuple[float, float]:
    source = PROJECT_DIR / "preliminary_wheel_drive_spec.json"
    raw_spec = json.loads(source.read_text(encoding="utf-8"))
    spec = validate_model_spec(raw_spec)
    shaft = next(
        component
        for component in spec["components"]
        if component["name"] == "Drive Shaft Placeholder"
    )
    if shaft["type"] != "cylinder" or shaft["axis"] != "y":
        raise ValueError("The preliminary shaft must remain a cylinder on axis Y.")
    dimensions = shaft["dimensions_mm"]
    return dimensions["diameter"], dimensions["height"]


def build_drawing(diameter_mm: float, length_mm: float) -> ShaftDrawing:
    drawing = ShaftDrawing()

    # A4 landscape border and drawing heading.
    drawing.rectangle(8, 8, 281, 194, "FRAME")
    drawing.text(14, 192, "WHEEL DRIVE BENCH DEMONSTRATOR", 3.4)
    drawing.text(
        14, 184, "PRELIMINARY - WORKFLOW TEST - NOT FOR MANUFACTURE", 2.4
    )
    drawing.line(14, 179, 283, 179, "FRAME")

    # Shaft side elevation: one plain cylindrical envelope, shown at 1:1.
    side_x = 48.0
    side_y = 90.0
    drawing.rectangle(side_x, side_y, length_mm, diameter_mm, "OUTLINE")
    drawing.text(side_x, 103, "SIDE VIEW", 2.3)

    # Centerline is shown as a simple dashed line for DXF compatibility.
    center_y = side_y + diameter_mm / 2
    center_start = side_x - 4
    center_end = side_x + length_mm + 4
    dash = 2.0
    gap = 1.5
    cursor = center_start
    while cursor < center_end:
        dash_end = min(cursor + dash, center_end)
        drawing.line(cursor, center_y, dash_end, center_y, "DIMENSIONS")
        cursor = dash_end + gap

    drawing.horizontal_dimension(
        side_x, side_x + length_mm, side_y, 73, f"{length_mm:g}"
    )

    # End view and a plain-text diameter leader.
    end_x = 140.0
    end_y = center_y
    radius = diameter_mm / 2
    drawing.circle(end_x, end_y, radius, "OUTLINE")
    drawing.line(end_x - 5, end_y, end_x + 5, end_y, "DIMENSIONS")
    drawing.line(end_x, end_y - 5, end_x, end_y + 5, "DIMENSIONS")
    drawing.text(end_x - 5, 103, "END VIEW", 2.3)
    drawing.line(end_x + radius * 0.72, end_y + radius * 0.72, 151, 99, "DIMENSIONS")
    drawing.line(151, 99, 160, 99, "DIMENSIONS")
    drawing.text(161, 99.7, f"DIA {diameter_mm:g}", 2.0, "DIMENSIONS")

    # Notes make the limits of the test part explicit.
    drawing.text(48, 59, "STRAIGHT CYLINDER ONLY", 2.2)
    drawing.text(
        48,
        54,
        "End form, material, tolerance, finish, and retention are unspecified.",
        1.8,
    )
    drawing.text(
        48,
        49,
        "Dimensions are provisional values from the A0 concept, not confirmed parts.",
        1.8,
    )
    drawing.text(48, 44, "Model axis: +Y. Dimensions in millimetres.", 1.8)

    # Compact title block.
    title_x, title_y, title_w, title_h = 174.0, 14.0, 110.0, 32.0
    drawing.rectangle(title_x, title_y, title_w, title_h, "FRAME")
    drawing.line(title_x, 34, title_x + title_w, 34, "FRAME")
    drawing.line(title_x + 69, title_y, title_x + 69, title_y + title_h, "FRAME")
    drawing.line(title_x, 24, title_x + title_w, 24, "FRAME")
    drawing.text(title_x + 3, 40, "DRIVE SHAFT - WORKFLOW TEST", 2.2)
    drawing.text(title_x + 3, 36, "PRELIMINARY / UNCONFIRMED", 1.8)
    drawing.text(title_x + 3, 28, "UNITS: mm   SCALE: 1:1", 1.8)
    drawing.text(title_x + 72, 28, "REV: A0", 1.8)
    drawing.text(title_x + 3, 18, "DIA / LENGTH", 1.8)
    drawing.text(title_x + 28, 18, f"{diameter_mm:g} / {length_mm:g}", 1.8)
    drawing.text(title_x + 72, 18, "WD-SHAFT-A0", 1.8)

    return drawing


def main() -> None:
    diameter_mm, length_mm = load_shaft_dimensions()
    drawing = build_drawing(diameter_mm, length_mm)
    dxf_text = drawing.dxf.render()
    svg_text = drawing.render_svg()

    dxf_path = HERE / "shaft_6x46_A0.dxf"
    html_path = HERE / "shaft_6x46_A0_preview.html"
    dxf_path.write_text(dxf_text, encoding="ascii")

    dxf_download = "data:application/dxf;charset=utf-8," + quote(dxf_text, safe="")
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Preliminary shaft drawing — A0 workflow test</title>
  <style>
    :root {{ color-scheme: light; font-family: Arial, sans-serif; }}
    body {{ margin: 0; background: #eef1f4; color: #18212b; }}
    main {{ max-width: 1320px; margin: 24px auto; padding: 0 18px; }}
    .notice {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
      justify-content: space-between; margin-bottom: 14px; }}
    .notice strong {{ color: #8c2f21; }}
    .download {{ padding: 10px 14px; background: #173b60; color: white;
      text-decoration: none; border-radius: 6px; font-weight: 700; }}
    .sheet {{ background: white; box-shadow: 0 8px 32px #15283b22; overflow: auto; }}
    svg {{ display: block; width: 100%; height: auto; }}
    p {{ line-height: 1.5; color: #495665; }}
  </style>
</head>
<body>
  <main>
    <div class="notice">
      <strong>PRELIMINARY — WORKFLOW TEST — NOT FOR MANUFACTURE</strong>
      <a class="download" href="{dxf_download}" download="shaft_6x46_A0.dxf">
        Download editable DXF for Fusion
      </a>
    </div>
    <section class="sheet" aria-label="Dimensioned shaft drawing">
      {svg_text}
    </section>
    <p>
      Provisional test geometry: diameter {diameter_mm:g} mm × length
      {length_mm:g} mm. This is a neutral DXF drawing sheet; its annotations
      are drawn geometry, not associative Fusion dimensions.
    </p>
  </main>
</body>
</html>
"""
    html_path.write_text(html_text, encoding="utf-8")
    print(f"Wrote {dxf_path}")
    print(f"Wrote {html_path}")
    print(
        f"Source dimensions: diameter {diameter_mm:g} mm, length {length_mm:g} mm "
        "(provisional)"
    )


if __name__ == "__main__":
    main()
