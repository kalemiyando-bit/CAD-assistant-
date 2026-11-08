#!/usr/bin/env python3
"""Create and verify a SHA-256 manifest for an engineering release folder.

This checks package integrity, not engineering correctness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA_VERSION = 1
DEFAULT_MANIFEST = "RELEASE-MANIFEST.json"
CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_relative_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"Unsafe or invalid relative path: {value!r}")
    return path


def resolve_manifest_path(root: Path, manifest_name: str) -> Path:
    relative = safe_relative_path(manifest_name)
    manifest_path = root.joinpath(*relative.parts)
    if manifest_path.resolve().parent != root.resolve() and root.resolve() not in manifest_path.resolve().parents:
        raise ValueError("Manifest path must remain inside the package directory.")
    return manifest_path


def package_files(root: Path, manifest_path: Path) -> list[Path]:
    files: list[Path] = []
    manifest_resolved = manifest_path.resolve()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Symbolic links are not allowed in a release package: {path.relative_to(root)}")
        if path.is_file() and path.resolve() != manifest_resolved:
            files.append(path)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def create_manifest(root: Path, manifest_name: str = DEFAULT_MANIFEST) -> dict[str, Any]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Package path is not a directory: {root}")
    manifest_path = resolve_manifest_path(root, manifest_name)
    if manifest_path.is_symlink():
        raise ValueError("Manifest path must not be a symbolic link.")

    entries: list[dict[str, Any]] = []
    for path in package_files(root, manifest_path):
        size = path.stat().st_size
        if size == 0:
            raise ValueError(f"Empty file cannot be included in a release: {path.relative_to(root)}")
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size_bytes": size,
                "sha256": sha256_file(path),
            }
        )

    if not entries:
        raise ValueError("No non-empty deliverable files found in the package directory.")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=manifest_path.parent,
            prefix=f".{manifest_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary_name = stream.name
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary_name, manifest_path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)
    return manifest


def verify_manifest(root: Path, manifest_name: str = DEFAULT_MANIFEST) -> list[str]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError(f"Package path is not a directory: {root}")
    manifest_path = resolve_manifest_path(root, manifest_name)
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError(f"Manifest file not found or unsafe: {manifest_name}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read manifest: {error}") from error
    if manifest.get("schema_version") != SCHEMA_VERSION or not isinstance(manifest.get("files"), list):
        raise ValueError("Unsupported or malformed manifest.")

    expected: dict[str, dict[str, Any]] = {}
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise ValueError("Malformed file entry in manifest.")
        relative = safe_relative_path(entry["path"]).as_posix()
        if relative in expected:
            raise ValueError(f"Duplicate file entry in manifest: {relative}")
        expected[relative] = entry

    actual_paths = {
        path.relative_to(root).as_posix(): path
        for path in package_files(root, manifest_path)
    }
    problems: list[str] = []

    for relative, entry in expected.items():
        path = actual_paths.get(relative)
        if path is None:
            problems.append(f"MISSING: {relative}")
            continue
        size = path.stat().st_size
        if size == 0:
            problems.append(f"EMPTY: {relative}")
            continue
        if size != entry.get("size_bytes") or sha256_file(path) != entry.get("sha256"):
            problems.append(f"CHANGED: {relative}")

    for relative in sorted(set(actual_paths) - set(expected)):
        problems.append(f"UNLISTED: {relative}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("create", "verify"))
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Manifest path relative to package_dir.")
    args = parser.parse_args()

    try:
        if args.command == "create":
            manifest = create_manifest(args.package_dir, args.manifest)
            print(f"Created {args.manifest}: {len(manifest['files'])} file(s) recorded.")
            return 0

        problems = verify_manifest(args.package_dir, args.manifest)
        if problems:
            for problem in problems:
                print(problem)
            print(f"FAIL: {len(problems)} package integrity issue(s).")
            return 1
        manifest_path = resolve_manifest_path(args.package_dir.resolve(), args.manifest)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        print(f"PASS: {len(manifest['files'])} file(s) match the manifest.")
        return 0
    except (OSError, ValueError) as error:
        parser.exit(2, f"error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
