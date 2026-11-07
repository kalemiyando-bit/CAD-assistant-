from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PILOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_DIR))

from fusion_model_spec import SpecValidationError, safe_file_stem, validate_model_spec


def box_spec():
    return {
        "schema_version": 1,
        "design_name": "Test Block",
        "units": "mm",
        "coordinate_system": "right-handed-z-up",
        "components": [
            {
                "name": "Block",
                "type": "box",
                "origin_mm": [0, 0, 0],
                "dimensions_mm": {"length": 100, "width": 60, "height": 40},
            }
        ],
    }


class FusionModelSpecTests(unittest.TestCase):
    def test_example_spec_is_valid(self):
        example_path = PILOT_DIR / "example_model_spec.json"
        normalized = validate_model_spec(
            json.loads(example_path.read_text(encoding="utf-8"))
        )
        self.assertEqual(normalized["components"][0]["dimensions_mm"]["length"], 100)

    def test_normalizes_numeric_values(self):
        normalized = validate_model_spec(box_spec())
        self.assertEqual(normalized["components"][0]["origin_mm"], [0.0, 0.0, 0.0])

    def test_cylinder_is_supported(self):
        spec = box_spec()
        spec["components"] = [
            {
                "name": "Shaft",
                "type": "cylinder",
                "origin_mm": [0, 0, 0],
                "dimensions_mm": {"diameter": 12, "height": 100},
            }
        ]
        self.assertEqual(
            validate_model_spec(spec)["components"][0]["type"], "cylinder"
        )

    def test_rejects_wrong_units(self):
        spec = box_spec()
        spec["units"] = "inch"
        with self.assertRaisesRegex(SpecValidationError, "millimetres"):
            validate_model_spec(spec)

    def test_rejects_unsupported_coordinate_system(self):
        spec = box_spec()
        spec["coordinate_system"] = "left-handed"
        with self.assertRaisesRegex(SpecValidationError, "right-handed-z-up"):
            validate_model_spec(spec)

    def test_rejects_zero_or_negative_dimensions(self):
        for value in (0, -1):
            spec = box_spec()
            spec["components"][0]["dimensions_mm"]["height"] = value
            with self.subTest(value=value):
                with self.assertRaisesRegex(SpecValidationError, "greater than zero"):
                    validate_model_spec(spec)

    def test_rejects_non_finite_dimensions(self):
        spec = box_spec()
        spec["components"][0]["dimensions_mm"]["width"] = float("nan")
        with self.assertRaisesRegex(SpecValidationError, "finite"):
            validate_model_spec(spec)

    def test_rejects_duplicate_component_names(self):
        spec = box_spec()
        duplicate = dict(spec["components"][0])
        duplicate["name"] = "block"
        spec["components"].append(duplicate)
        with self.assertRaisesRegex(SpecValidationError, "unique"):
            validate_model_spec(spec)

    def test_rejects_missing_origin_coordinate(self):
        spec = box_spec()
        spec["components"][0]["origin_mm"] = [0, 0]
        with self.assertRaisesRegex(SpecValidationError, "x, y, z"):
            validate_model_spec(spec)

    def test_rejects_unsupported_component_type(self):
        spec = box_spec()
        spec["components"][0]["type"] = "mesh"
        with self.assertRaisesRegex(SpecValidationError, "box, cylinder"):
            validate_model_spec(spec)

    def test_filename_stem_cannot_escape_a_folder(self):
        self.assertEqual(safe_file_stem("../../Robot: V1"), "robot-v1")


if __name__ == "__main__":
    unittest.main()
