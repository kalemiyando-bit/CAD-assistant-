"""Pure helpers for selecting one or more Fusion model-spec files."""

from __future__ import annotations

import os
from collections.abc import Iterable


def normalize_selected_spec_paths(
    selected_paths: Iterable[str] | str | None,
    single_path: str | None = None,
) -> list[str]:
    """Return unique selected paths in selection order.

    Fusion versions may expose the multi-selection as ``filenames`` while
    single-selection callers and test doubles may expose only ``filename``.
    """
    if isinstance(selected_paths, str):
        paths = [selected_paths]
    else:
        paths = list(selected_paths or [])

    if not paths and single_path:
        paths = [single_path]

    normalized: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if not path:
            continue
        identity = os.path.normcase(os.path.normpath(path))
        if identity in seen:
            continue
        seen.add(identity)
        normalized.append(path)
    return normalized


def ensure_output_folder(path: str) -> str:
    """Create the configured output directory and return its normalized path."""
    if not path or not path.strip():
        raise ValueError("An output folder path must be configured.")
    normalized_path = os.path.normpath(path)
    os.makedirs(normalized_path, exist_ok=True)
    if not os.path.isdir(normalized_path):
        raise NotADirectoryError(
            f"The configured output path is not a directory: {normalized_path}"
        )
    return normalized_path
