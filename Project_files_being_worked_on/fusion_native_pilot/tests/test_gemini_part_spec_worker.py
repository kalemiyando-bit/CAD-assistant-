"""Focused offline checks for the Gemini worker's API contract."""

from __future__ import annotations

import json
import sys
import unittest
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError
from unittest.mock import patch


PILOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_DIR))

import gemini_part_spec_worker as worker  # noqa: E402


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def ready_response() -> dict:
    result = {
        "status": "draft_ready",
        "summary": "A preliminary cylindrical part.",
        "questions": [],
        "unsupported_reason": "",
        "dimension_basis": [
            {
                "field": "components[0].dimensions_mm.diameter",
                "basis": "user_brief",
                "note": "Diameter supplied in the brief.",
            },
            {
                "field": "components[0].dimensions_mm.height",
                "basis": "user_brief",
                "note": "Height supplied in the brief.",
            },
        ],
        "model_spec": {
            "schema_version": 1,
            "design_name": "Offline API Contract Test",
            "design_status": "PRELIMINARY_CONCEPT",
            "assumptions": [],
            "units": "mm",
            "coordinate_system": "right-handed-z-up",
            "components": [
                {
                    "name": "Test cylinder",
                    "type": "cylinder",
                    "axis": "z",
                    "origin_mm": [0, 0, 0],
                    "dimensions_mm": {"diameter": 10, "height": 20},
                }
            ],
        },
    }
    return result


class GeminiPartSpecWorkerTests(unittest.TestCase):
    def test_provider_error_details_are_kept_and_api_key_is_redacted(self) -> None:
        body = json.dumps(
            {
                "error": {
                    "code": 400,
                    "status": "INVALID_ARGUMENT",
                    "details": [{"message": "schema rejected"}],
                }
            }
        ).encode("utf-8")
        error = HTTPError(
            "https://example.invalid",
            400,
            "Bad Request",
            {},
            BytesIO(body),
        )

        message = worker._api_error_message(error, "test-secret-value")

        self.assertIn("INVALID_ARGUMENT", message)
        self.assertIn("schema rejected", message)
        self.assertNotIn("test-secret-value", message)

    def test_uses_gemini_rest_structured_output_fields_and_validates_result(self) -> None:
        generated = ready_response()
        api_response = {
            "candidates": [
                {
                    "finishReason": "STOP",
                    "content": {
                        "parts": [{"text": json.dumps(generated)}],
                    },
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 30,
                "candidatesTokenCount": 50,
                "totalTokenCount": 80,
            },
        }
        captured: dict[str, object] = {}

        def fake_urlopen(request, timeout: int) -> FakeResponse:
            captured["url"] = request.full_url
            captured["timeout"] = timeout
            captured["payload"] = json.loads(request.data.decode("utf-8"))
            return FakeResponse(api_response)

        with patch.object(worker, "urlopen", side_effect=fake_urlopen):
            result, usage = worker._call_gemini(
                {
                    "design_name": "Offline API Contract Test",
                    "design_brief": "A 10 mm diameter cylinder, 20 mm tall.",
                    "approved_assumptions": [],
                },
                "gemini-3.8-flash",
                "test-key-not-a-real-credential",
            )

        payload = captured["payload"]
        self.assertIsInstance(payload, dict)
        config = payload["generationConfig"]
        self.assertEqual(config["responseMimeType"], "application/json")
        self.assertEqual(config["responseSchema"], worker.GEMINI_OUTPUT_SCHEMA)
        self.assertNotIn("responseFormat", config)
        self.assertEqual(
            config["responseSchema"]["type"],
            "OBJECT",
        )
        self.assertNotIn(
            "enum",
            config["responseSchema"]["properties"]["model_spec"]["properties"][
                "schema_version"
            ],
        )
        self.assertEqual(
            config["responseSchema"]["properties"]["questions"]["type"],
            "ARRAY",
        )
        self.assertEqual(
            config["responseSchema"]["properties"]["questions"]["items"]["type"],
            "STRING",
        )
        component_variants = config["responseSchema"]["properties"]["model_spec"][
            "properties"
        ]["components"]["items"]["anyOf"]
        dimensions_by_type = {
            variant["properties"]["type"]["enum"][0]: variant["properties"][
                "dimensions_mm"
            ]["properties"]
            for variant in component_variants
        }
        self.assertEqual(
            set(dimensions_by_type["box"]),
            {"length", "width", "height"},
        )
        self.assertEqual(
            set(dimensions_by_type["cylinder"]),
            {"diameter", "height"},
        )
        for variant in component_variants:
            self.assertNotIn("additionalProperties", variant)
            self.assertNotIn(
                "additionalProperties",
                variant["properties"]["dimensions_mm"],
            )
        self.assertEqual(captured["timeout"], worker.API_TIMEOUT_SECONDS)
        self.assertEqual(usage["total_tokens"], 80)
        self.assertEqual(worker._validate_output(result)["status"], "draft_ready")


if __name__ == "__main__":
    unittest.main()
