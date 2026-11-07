from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SHAFT_TEST_DIR = PROJECT_DIR / "shaft_2d_test"
sys.path.insert(0, str(SHAFT_TEST_DIR))

from generate_shaft_drawing import build_drawing, load_shaft_dimensions


class ShaftDrawingTests(unittest.TestCase):
    def test_dimensions_come_from_preliminary_model_spec(self) -> None:
        self.assertEqual(load_shaft_dimensions(), (6.0, 46.0))

    def test_dxf_is_mm_and_contains_both_views_and_annotations(self) -> None:
        diameter, length = load_shaft_dimensions()
        dxf_text = build_drawing(diameter, length).render_r12_dxf()
        lines = dxf_text.splitlines()
        self.assertEqual(len(lines) % 2, 0)
        pairs = list(zip(lines[::2], lines[1::2]))
        self.assertEqual(pairs[-1], ("0", "EOF"))
        self.assertIn(("1", "AC1009"), pairs)

        units_index = pairs.index(("9", "$INSUNITS"))
        self.assertEqual(pairs[units_index + 1], ("70", "4"))
        self.assertNotIn(("2", "TABLES"), pairs)

        for label in (
            "SIDE VIEW",
            "END VIEW",
            "DIA 6",
            "PRELIMINARY - WORKFLOW TEST - NOT FOR MANUFACTURE",
        ):
            self.assertIn(label, dxf_text)

        self.assertGreaterEqual(dxf_text.count("\nLINE\n"), 20)
        self.assertIn("\nCIRCLE\n", dxf_text)

    def test_preview_svg_matches_the_model_dimensions(self) -> None:
        diameter, length = load_shaft_dimensions()
        svg = build_drawing(diameter, length).render_svg()
        self.assertIn("<svg ", svg)
        self.assertIn(">46</text>", svg)
        self.assertIn(">DIA 6</text>", svg)
        self.assertIn("NOT FOR MANUFACTURE", svg)


if __name__ == "__main__":
    unittest.main()
