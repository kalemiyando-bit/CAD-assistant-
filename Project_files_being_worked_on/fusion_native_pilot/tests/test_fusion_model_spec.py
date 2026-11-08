from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PILOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_DIR))

from fusion_model_spec import (
    SpecValidationError,
    expected_component_extents_mm,
    safe_file_stem,
    validate_model_spec,
)


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

    def test_wheel_drive_preliminary_spec_is_valid(self):
        concept_path = (
            PILOT_DIR.parent / "wheel_drive_bench_demo"
            / "preliminary_wheel_drive_spec.json"
        )
        normalized = validate_model_spec(
            json.loads(concept_path.read_text(encoding="utf-8"))
        )
        self.assertEqual(normalized["design_status"], "PRELIMINARY_CONCEPT")
        self.assertEqual(len(normalized["components"]), 7)
        wheel = normalized["components"][0]
        self.assertEqual(expected_component_extents_mm(wheel), [80.0, 24.0, 80.0])

    def test_single_shaft_model_spec_is_valid_and_one_component(self):
        shaft_spec_path = (
            PILOT_DIR.parent
            / "wheel_drive_bench_demo"
            / "shaft_2d_test"
            / "shaft_6x46_A0_model_spec.json"
        )
        normalized = validate_model_spec(
            json.loads(shaft_spec_path.read_text(encoding="utf-8"))
        )

        self.assertEqual(normalized["design_status"], "PRELIMINARY_CONCEPT")
        self.assertEqual(len(normalized["components"]), 1)
        shaft = normalized["components"][0]
        self.assertEqual(shaft["name"], "Drive Shaft Placeholder")
        self.assertEqual(shaft["type"], "cylinder")
        self.assertEqual(shaft["axis"], "y")
        self.assertEqual(shaft["origin_mm"], [0.0, 0.0, 0.0])
        self.assertEqual(
            shaft["dimensions_mm"], {"diameter": 6.0, "height": 46.0}
        )

    def test_axis_alignment_maps_local_dimensions_to_world_axes(self):
        support = {
            "type": "plate_with_bore",
            "axis": "y",
            "dimensions_mm": {
                "length": 30,
                "width": 30,
                "height": 4,
                "bore_diameter": 12,
            },
        }
        self.assertEqual(expected_component_extents_mm(support), [30, 4, 30])

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

    def test_annular_cylinder_is_supported_and_normalized(self):
        spec = box_spec()
        spec["components"] = [
            {
                "name": "Wheel Rim",
                "type": "annular_cylinder",
                "axis": "y",
                "origin_mm": [0, 4, 50],
                "dimensions_mm": {
                    "outer_diameter": 80,
                    "inner_diameter": 6,
                    "height": 24,
                },
            }
        ]
        normalized = validate_model_spec(spec)
        self.assertEqual(normalized["components"][0]["axis"], "y")
        self.assertEqual(
            normalized["components"][0]["dimensions_mm"]["outer_diameter"], 80.0
        )

    def test_plate_with_bore_is_supported(self):
        spec = box_spec()
        spec["components"] = [
            {
                "name": "Bearing Support",
                "type": "plate_with_bore",
                "axis": "y",
                "origin_mm": [-15, 0, 65],
                "dimensions_mm": {
                    "length": 30,
                    "width": 30,
                    "height": 4,
                    "bore_diameter": 12,
                },
            }
        ]
        self.assertEqual(
            validate_model_spec(spec)["components"][0]["type"], "plate_with_bore"
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
        with self.assertRaisesRegex(
            SpecValidationError, "annular_cylinder, box, cylinder, plate_with_bore"
        ):
            validate_model_spec(spec)

    def test_rejects_invalid_axis(self):
        spec = box_spec()
        spec["components"][0]["axis"] = "diagonal"
        with self.assertRaisesRegex(SpecValidationError, "axis must be one of"):
            validate_model_spec(spec)

    def test_rejects_annular_cylinder_with_no_wall(self):
        spec = box_spec()
        spec["components"] = [
            {
                "name": "Invalid Ring",
                "type": "annular_cylinder",
                "origin_mm": [0, 0, 0],
                "dimensions_mm": {
                    "outer_diameter": 12,
                    "inner_diameter": 12,
                    "height": 4,
                },
            }
        ]
        with self.assertRaisesRegex(SpecValidationError, "smaller than outer_diameter"):
            validate_model_spec(spec)

    def test_rejects_plate_bore_larger_than_plate(self):
        spec = box_spec()
        spec["components"] = [
            {
                "name": "Invalid Support",
                "type": "plate_with_bore",
                "origin_mm": [0, 0, 0],
                "dimensions_mm": {
                    "length": 20,
                    "width": 16,
                    "height": 4,
                    "bore_diameter": 16,
                },
            }
        ]
        with self.assertRaisesRegex(SpecValidationError, "smaller than both plate"):
            validate_model_spec(spec)

    def test_filename_stem_cannot_escape_a_folder(self):
        self.assertEqual(safe_file_stem("../../Robot: V1"), "robot-v1")


if __name__ == "__main__":
    unittest.main()
