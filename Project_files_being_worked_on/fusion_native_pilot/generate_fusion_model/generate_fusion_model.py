"""Fusion add-in entry point; the implementation is shared in the pilot folder."""

from __future__ import annotations

import importlib.util
import os
import sys


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PILOT_DIR = os.path.dirname(SCRIPT_DIR)
if PILOT_DIR not in sys.path:
    sys.path.insert(0, PILOT_DIR)

CORE_PATH = os.path.join(PILOT_DIR, "generate_fusion_model.py")
CORE_SPEC = importlib.util.spec_from_file_location(
    "_cad_assistant_fusion_model_generator", CORE_PATH
)
if not CORE_SPEC or not CORE_SPEC.loader:
    raise RuntimeError("Could not load the Fusion model generator implementation.")
CORE_MODULE = importlib.util.module_from_spec(CORE_SPEC)
CORE_SPEC.loader.exec_module(CORE_MODULE)


def run(context):
    CORE_MODULE.run(context)
