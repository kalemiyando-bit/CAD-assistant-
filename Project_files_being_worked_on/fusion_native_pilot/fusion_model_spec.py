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
SUPPORTED_TYPES = {"box", "cylinder", "annular_cylinder", "plate_with_bore"}
SUPPORTED_AXES = {"x", "y", "z"}


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


def expected_component_extents_mm(component: dict[str, Any]) -> list[float]:
    """Return principal-axis extents after the component's X/Y/Z axis alignment."""
    dimensions = component["dimensions_mm"]
    component_type = component["type"]
    if component_type in {"box", "plate_with_bore"}:
        local_extents = [
            dimensions["length"],
            dimensions["width"],
            dimensions["height"],
        ]
    elif component_type == "cylinder":
        local_extents = [
            dimensions["diameter"],
            dimensions["diameter"],
            dimensions["height"],
        ]
    elif component_type == "annular_cylinder":
        outer_diameter = dimensions["outer_diameter"]
        local_extents = [outer_diameter, outer_diameter, dimensions["height"]]
    else:
        raise SpecValidationError(
            f"Cannot calculate extents for unsupported type: {component_type!r}."
        )

    axis = component.get("axis", "z")
    if axis == "x":
        return [local_extents[2], local_extents[1], local_extents[0]]
    if axis == "y":
        return [local_extents[0], local_extents[2], local_extents[1]]
    if axis == "z":
        return local_extents
    raise SpecValidationError(f"Unsupported component axis: {axis!r}.")


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

    design_status = payload.get("design_status", "PRELIMINARY_CONCEPT")
    if (
        not isinstance(design_status, str)
        or not design_status.strip()
        or len(design_status) > 40
    ):
        raise SpecValidationError(
            "design_status must be a non-empty string of at most 40 characters."
        )
    design_status = design_status.strip()

    assumptions = payload.get("assumptions", [])
    if not isinstance(assumptions, list) or any(
        not isinstance(item, str) or not item.strip() for item in assumptions
    ):
        raise SpecValidationError("assumptions must be an array of non-empty strings.")
    if len(assumptions) > 50:
        raise SpecValidationError("At most 50 design assumptions are supported.")
    assumptions = [item.strip() for item in assumptions]

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
        if not isinstance(component_type, str) or component_type not in SUPPORTED_TYPES:
            allowed = ", ".join(sorted(SUPPORTED_TYPES))
            raise SpecValidationError(
                f"{prefix}.type must be one of: {allowed}."
            )

        axis = component.get("axis", "z")
        if not isinstance(axis, str) or axis not in SUPPORTED_AXES:
            raise SpecValidationError(
                f"{prefix}.axis must be one of: {', '.join(sorted(SUPPORTED_AXES))}."
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

        required_dimensions = {
            "box": ("length", "width", "height"),
            "cylinder": ("diameter", "height"),
            "annular_cylinder": ("outer_diameter", "inner_diameter", "height"),
            "plate_with_bore": ("length", "width", "height", "bore_diameter"),
        }[component_type]
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

        if (
            component_type == "annular_cylinder"
            and normalized_dimensions["inner_diameter"]
            >= normalized_dimensions["outer_diameter"]
        ):
            raise SpecValidationError(
                f"{prefix}.dimensions_mm.inner_diameter must be smaller than "
                "outer_diameter."
            )
        if component_type == "plate_with_bore" and normalized_dimensions[
            "bore_diameter"
        ] >= min(
            normalized_dimensions["length"], normalized_dimensions["width"]
        ):
            raise SpecValidationError(
                f"{prefix}.dimensions_mm.bore_diameter must be smaller than both "
                "plate dimensions."
            )

        normalized_components.append(
            {
                "name": name,
                "type": component_type,
                "axis": axis,
                "origin_mm": origin_values,
                "dimensions_mm": normalized_dimensions,
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "design_name": design_name,
        "design_status": design_status,
        "assumptions": assumptions,
        "units": "mm",
        "coordinate_system": "right-handed-z-up",
        "components": normalized_components,
    }
