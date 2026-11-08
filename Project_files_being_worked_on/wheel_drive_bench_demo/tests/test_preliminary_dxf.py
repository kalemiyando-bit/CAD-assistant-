from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
PILOT_DIR = PROJECT_DIR.parent / "fusion_native_pilot"
sys.path.insert(0, str(PILOT_DIR))
sys.path.insert(0, str(PROJECT_DIR))

from fusion_model_spec import validate_model_spec
from generate_preliminary_dxf import build_dxf


class PreliminaryDxfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        payload = json.loads(
            (PROJECT_DIR / "preliminary_wheel_drive_spec.json").read_text(
                encoding="utf-8"
            )
        )
        cls.spec = validate_model_spec(payload)
        cls.dxf = build_dxf(cls.spec)
        cls.pairs = list(zip(cls.dxf.splitlines()[::2], cls.dxf.splitlines()[1::2]))

    def test_group_code_lines_are_paired_and_file_is_closed(self):
        self.assertEqual(len(self.dxf.splitlines()) % 2, 0)
        self.assertTrue(self.dxf.endswith("0\nEOF\n"))

    def test_declares_millimetres_and_ascii_output(self):
        self.assertIn("$INSUNITS\n70\n4\n", self.dxf)
        self.assertIn("UNITS: MM", self.dxf)
        self.assertTrue(self.dxf.isascii())

    def test_each_concept_component_has_a_panel(self):
        labels = (
            "Wheel rim",
            "Wheel hub",
            "Drive shaft",
            "Bearing envelope",
            "Bearing support plate",
            "Coupling envelope",
            "Motor body envelope",
        )
        for label in labels:
            with self.subTest(label=label):
                self.assertIn(label, self.dxf)
        self.assertIn("NOT FOR MANUFACTURE", self.dxf)

    def test_key_dimensions_and_open_interfaces_are_shown(self):
        self.assertIn("DIA 80", self.dxf)
        self.assertIn("BORE DIA 6", self.dxf)
        self.assertIn("OD 12 / ID 6", self.dxf)
        self.assertIn("BORES UNSPECIFIED", self.dxf)
        self.assertIn("NO TOLERANCES", self.dxf)

    def test_expected_entity_types_are_written(self):
        entity_types = [value for code, value in self.pairs if code == "0"]
        self.assertGreaterEqual(entity_types.count("CIRCLE"), 8)
        self.assertGreaterEqual(entity_types.count("LINE"), 100)
        self.assertGreaterEqual(entity_types.count("TEXT"), 20)


if __name__ == "__main__":
    unittest.main()
