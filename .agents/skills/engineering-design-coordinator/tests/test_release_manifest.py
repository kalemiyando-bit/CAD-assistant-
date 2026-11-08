from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "release_manifest.py"


class ReleaseManifestTests(unittest.TestCase):
    def run_tool(self, command: str, folder: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), command, str(folder)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_create_and_verify_package(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "part.step").write_text("STEP content\n", encoding="utf-8")
            (root / "notes").mkdir()
            (root / "notes" / "handoff.txt").write_text("Units: mm\n", encoding="utf-8")

            created = self.run_tool("create", root)
            verified = self.run_tool("verify", root)

            self.assertEqual(created.returncode, 0, created.stderr + created.stdout)
            self.assertEqual(verified.returncode, 0, verified.stderr + verified.stdout)
            self.assertIn("2 file(s)", verified.stdout)

    def test_detects_changed_missing_and_unlisted_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "part.step").write_text("original\n", encoding="utf-8")
            (root / "drawing.pdf").write_text("sheet\n", encoding="utf-8")
            self.assertEqual(self.run_tool("create", root).returncode, 0)

            (root / "part.step").write_text("changed\n", encoding="utf-8")
            (root / "drawing.pdf").unlink()
            (root / "extra.txt").write_text("unexpected\n", encoding="utf-8")
            verified = self.run_tool("verify", root)

            self.assertEqual(verified.returncode, 1)
            self.assertIn("CHANGED: part.step", verified.stdout)
            self.assertIn("MISSING: drawing.pdf", verified.stdout)
            self.assertIn("UNLISTED: extra.txt", verified.stdout)

    def test_rejects_empty_deliverables(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "empty.step").touch()
            created = self.run_tool("create", root)
            self.assertEqual(created.returncode, 2)
            self.assertIn("Empty file", created.stderr)


if __name__ == "__main__":
    unittest.main()
