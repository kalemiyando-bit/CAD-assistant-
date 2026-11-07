"""Validation helpers for the Fusion model-spec pilot.

This module intentionally uses only Python's standard library so it can be
tested outside Fusion. The Fusion API script imports this same validator.
"""

from __future__ import annotations

import math
import re
import unicodedata
from typing import Any


SCHEMA_VERSION = 1
MAX_COMPONENTS = 50
MAX_NAME_LENGTH = 80
MAX_DIMENSION_MM = 10_000.0
MAX_ORIGIN_MM = 100_000.0
SUPPORTED_TYPES = {"box", "cylinder"}


class SpecValidationError(ValueError):
    """Raised when a model specification is incomplete or unsafe to build."""


def _number(value: Any, field_path: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecValidationError(f"{field_path} must be a number.")
    result = float(value)
    if not math.isfinite(result):
        raise SpecValidationError(f"{field_path} must be finite.")
    if positive and result <= 0:
        raise SpecValidationError(f"{field_path} must be greater than zero.")
    return result


def safe_file_stem(value: str) -> str:
    """Return a conservative filename stem without path separators."""
    ascii_value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    slug = re.sub(r"[^A-Za-z0-9]+", "-", ascii_value).strip("-").lower()
    return slug[:80].strip("-") or "fusion-design"


def validate_model_spec(payload: Any) -> dict[str, Any]:
    """Validate and normalize a version-1, millimetre-based Fusion model spec."""
    if not isinstance(payload, dict):
        raise SpecValidationError("The model specification must be a JSON object.")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise SpecValidationError(
            f"schema_version must be {SCHEMA_VERSION}."
        )

    design_name = payload.get("design_name")
    if not isinstance(design_name, str) or not design_name.strip():
        raise SpecValidationError("design_name must be a non-empty string.")
    design_name = design_name.strip()
    if len(design_name) > MAX_NAME_LENGTH:
        raise SpecValidationError(
            f"design_name must be {MAX_NAME_LENGTH} characters or fewer."
        )

    if payload.get("units") != "mm":
        raise SpecValidationError("Only millimetres (units: 'mm') are supported.")
    if payload.get("coordinate_system") != "right-handed-z-up":
        raise SpecValidationError(
            "coordinate_system must be 'right-handed-z-up'."
        )

    components = payload.get("components")
    if not isinstance(components, list) or not components:
        raise SpecValidationError("components must be a non-empty array.")
    if len(components) > MAX_COMPONENTS:
        raise SpecValidationError(
            f"At most {MAX_COMPONENTS} components are supported per model."
        )

    normalized_components: list[dict[str, Any]] = []
    used_names: set[str] = set()

    for index, component in enumerate(components, start=1):
        prefix = f"components[{index - 1}]"
        if not isinstance(component, dict):
            raise SpecValidationError(f"{prefix} must be an object.")

        name = component.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SpecValidationError(f"{prefix}.name must be a non-empty string.")
        name = name.strip()
        if len(name) > MAX_NAME_LENGTH:
            raise SpecValidationError(
                f"{prefix}.name must be {MAX_NAME_LENGTH} characters or fewer."
            )
        if name.casefold() in used_names:
            raise SpecValidationError(
                f"Component names must be unique; duplicate name: {name!r}."
            )
        used_names.add(name.casefold())

        component_type = component.get("type")
        if component_type not in SUPPORTED_TYPES:
            allowed = ", ".join(sorted(SUPPORTED_TYPES))
            raise SpecValidationError(
                f"{prefix}.type must be one of: {allowed}."
            )

        origin = component.get("origin_mm")
        if not isinstance(origin, list) or len(origin) != 3:
            raise SpecValidationError(
                f"{prefix}.origin_mm must contain [x, y, z] coordinates."
            )
        origin_values = [
            _number(value, f"{prefix}.origin_mm[{axis}]")
            for axis, value in enumerate(origin)
        ]
        if any(abs(value) > MAX_ORIGIN_MM for value in origin_values):
            raise SpecValidationError(
                f"{prefix}.origin_mm values must be within ±{MAX_ORIGIN_MM:g} mm."
            )

        dimensions = component.get("dimensions_mm")
        if not isinstance(dimensions, dict):
            raise SpecValidationError(f"{prefix}.dimensions_mm must be an object.")

        required_dimensions = (
            ("length", "width", "height")
            if component_type == "box"
            else ("diameter", "height")
        )
        normalized_dimensions: dict[str, float] = {}
        for key in required_dimensions:
            value = _number(
                dimensions.get(key),
                f"{prefix}.dimensions_mm.{key}",
                positive=True,
            )
            if value > MAX_DIMENSION_MM:
                raise SpecValidationError(
                    f"{prefix}.dimensions_mm.{key} exceeds {MAX_DIMENSION_MM:g} mm."
                )
            normalized_dimensions[key] = value

        normalized_components.append(
            {
                "name": name,
                "type": component_type,
                "origin_mm": origin_values,
                "dimensions_mm": normalized_dimensions,
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "design_name": design_name,
        "units": "mm",
        "coordinate_system": "right-handed-z-up",
        "components": normalized_components,
    }
