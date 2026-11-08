from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

PILOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_DIR))

from fusion_spec_batch import ensure_output_folder, normalize_selected_spec_paths


class FusionSpecBatchSelectionTests(unittest.TestCase):
    def test_keeps_multiple_paths_in_selection_order(self):
        paths = ["C:/models/wheel.json", "C:/models/hub.json"]
        self.assertEqual(normalize_selected_spec_paths(paths), paths)

    def test_falls_back_to_single_filename(self):
        self.assertEqual(
            normalize_selected_spec_paths([], "C:/models/shaft.json"),
            ["C:/models/shaft.json"],
        )

    def test_accepts_a_single_string_from_a_dialog(self):
        self.assertEqual(
            normalize_selected_spec_paths("C:/models/wheel.json"),
            ["C:/models/wheel.json"],
        )

    def test_removes_duplicate_paths_without_reordering(self):
        paths = [
            "C:/models/wheel.json",
            "C:/models/./wheel.json",
            "C:/models/hub.json",
        ]
        self.assertEqual(
            normalize_selected_spec_paths(paths),
            ["C:/models/wheel.json", "C:/models/hub.json"],
        )

    def test_empty_selection_returns_no_paths(self):
        self.assertEqual(normalize_selected_spec_paths(None), [])

    def test_creates_configured_output_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "CAD_Assistant" / "GENERATED"
            result = ensure_output_folder(str(output_path))
            self.assertTrue(output_path.is_dir())
            self.assertEqual(result, str(output_path))

    def test_rejects_empty_output_folder(self):
        with self.assertRaisesRegex(ValueError, "must be configured"):
            ensure_output_folder(" ")

    def test_rejects_a_file_as_output_folder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "not-a-folder"
            file_path.write_text("existing file", encoding="utf-8")
            with self.assertRaises(OSError):
                ensure_output_folder(str(file_path))


if __name__ == "__main__":
    unittest.main()
