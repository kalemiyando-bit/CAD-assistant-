"""Expose the shared model-spec validator to the Fusion add-in folder."""

from __future__ import annotations

import importlib.util
import os


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PILOT_DIR = os.path.dirname(SCRIPT_DIR)
CORE_PATH = os.path.join(PILOT_DIR, "fusion_model_spec.py")
CORE_SPEC = importlib.util.spec_from_file_location(
    "_cad_assistant_fusion_model_spec", CORE_PATH
)
if not CORE_SPEC or not CORE_SPEC.loader:
    raise RuntimeError("Could not load the Fusion model-spec validator.")
CORE_MODULE = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(CORE_MODULE)

expected_component_extents_mm = CORE_MODULE.expected_component_extents_mm
safe_file_stem = CORE_MODULE.safe_file_stem
validate_model_spec = CORE_MODULE.validate_model_spec
