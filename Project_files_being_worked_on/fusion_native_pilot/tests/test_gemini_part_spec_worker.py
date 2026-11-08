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
    def test_default_model_is_the_live_validated_candidate(self) -> None:
        self.assertEqual(worker.DEFAULT_MODEL, "gemini-3.6-flash")

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

        message, credential_rejected, quota_limited = worker._api_error_message(
            error,
            "test-secret-value",
        )

        self.assertIn("INVALID_ARGUMENT", message)
        self.assertIn("schema rejected", message)
        self.assertNotIn("test-secret-value", message)
        self.assertFalse(credential_rejected)
        self.assertFalse(quota_limited)

    def test_invalid_key_error_is_classified_for_serial_fallback(self) -> None:
        body = json.dumps(
            {
                "error": {
                    "code": 403,
                    "status": "PERMISSION_DENIED",
                    "message": "API key not valid. Please pass a valid API key.",
                }
            }
        ).encode("utf-8")
        error = HTTPError(
            "https://example.invalid",
            403,
            "Forbidden",
            {},
            BytesIO(body),
        )

        _, credential_rejected, quota_limited = worker._api_error_message(
            error,
            "fake-key",
        )

        self.assertTrue(credential_rejected)
        self.assertFalse(quota_limited)

    def test_http_429_is_classified_as_a_project_quota_limit(self) -> None:
        body = json.dumps(
            {
                "error": {
                    "code": 429,
                    "status": "RESOURCE_EXHAUSTED",
                    "message": "Quota exceeded.",
                }
            }
        ).encode("utf-8")
        error = HTTPError(
            "https://example.invalid",
            429,
            "Too Many Requests",
            {},
            BytesIO(body),
        )

        _, credential_rejected, quota_limited = worker._api_error_message(
            error,
            "fake-key",
        )

        self.assertFalse(credential_rejected)
        self.assertTrue(quota_limited)

    def test_configured_keys_keep_order_and_remove_duplicates(self) -> None:
        keys = worker._configured_api_keys(
            {
                "GEMINI_API_KEY": " first ",
                "GEMINI_API_KEY_2": "first",
                "GEMINI_API_KEY_3": "third",
            }
        )

        self.assertEqual(
            keys,
            [
                ("GEMINI_API_KEY", "first"),
                ("GEMINI_API_KEY_3", "third"),
            ],
        )

    def test_key_fallback_is_serial_and_only_on_explicit_rejection(self) -> None:
        request_data = {
            "design_name": "Offline API Contract Test",
            "design_brief": "A 10 mm diameter cylinder, 20 mm tall.",
            "approved_assumptions": [],
        }
        result_data = ready_response()
        usage_data = {"model": "gemini-3.8-flash", "total_tokens": 80}
        with patch.object(
            worker,
            "_call_gemini",
            side_effect=[
                worker.GeminiAPIError(
                    "Invalid API key",
                    credential_rejected=True,
                ),
                (result_data, usage_data),
            ],
        ) as call:
            result, usage = worker._call_gemini_with_keys(
                request_data,
                "gemini-3.8-flash",
                [
                    ("GEMINI_API_KEY", "fake-first-key"),
                    ("GEMINI_API_KEY_2", "fake-second-key"),
                ],
            )

        self.assertEqual(call.call_count, 2)
        self.assertEqual(result, result_data)
        self.assertEqual(usage["credential_env"], "GEMINI_API_KEY_2")

    def test_project_quota_fallback_tries_keys_in_order_until_success(self) -> None:
        request_data = {
            "design_name": "Offline API Contract Test",
            "design_brief": "A 10 mm diameter cylinder, 20 mm tall.",
            "approved_assumptions": [],
        }
        result_data = ready_response()
        usage_data = {"model": "gemini-3.6-flash", "total_tokens": 80}
        api_keys = [
            ("GEMINI_API_KEY", "fake-primary-key"),
            ("GEMINI_API_KEY_2", "fake-backup-key-2"),
            ("GEMINI_API_KEY_3", "fake-backup-key-3"),
        ]
        with patch.object(
            worker,
            "_call_gemini",
            side_effect=[
                worker.GeminiAPIError(
                    "Gemini API returned HTTP 429: project quota exceeded",
                    quota_limited=True,
                ),
                worker.GeminiAPIError(
                    "Gemini API returned HTTP 429: project quota exceeded",
                    quota_limited=True,
                ),
                (result_data, usage_data),
            ],
        ) as call:
            result, usage = worker._call_gemini_with_keys(
                request_data,
                "gemini-3.6-flash",
                api_keys,
            )

        self.assertEqual(call.call_count, 3)
        self.assertEqual(
            [entry.args[2] for entry in call.call_args_list],
            [key for _, key in api_keys],
        )
        self.assertEqual(result, result_data)
        self.assertEqual(usage["credential_env"], "GEMINI_API_KEY_3")

    def test_rate_or_provider_errors_do_not_try_another_key(self) -> None:
        with patch.object(
            worker,
            "_call_gemini",
            side_effect=worker.GeminiAPIError(
                "Gemini API returned HTTP 503: temporarily unavailable",
                credential_rejected=False,
            ),
        ) as call:
            with self.assertRaisesRegex(worker.GeminiAPIError, "HTTP 503"):
                worker._call_gemini_with_keys(
                    {
                        "design_name": "Offline API Contract Test",
                        "design_brief": "A 10 mm diameter cylinder, 20 mm tall.",
                        "approved_assumptions": [],
                    },
                    "gemini-3.8-flash",
                    [
                        ("GEMINI_API_KEY", "fake-first-key"),
                        ("GEMINI_API_KEY_2", "fake-second-key"),
                    ],
                )

        self.assertEqual(call.call_count, 1)

    def test_ready_output_requires_exact_dimension_provenance(self) -> None:
        missing = ready_response()
        missing["dimension_basis"].pop()
        with self.assertRaisesRegex(worker.WorkerError, "omitted the source"):
            worker._validate_output(missing)

        duplicate = ready_response()
        duplicate["dimension_basis"].append(duplicate["dimension_basis"][0].copy())
        with self.assertRaisesRegex(worker.WorkerError, "duplicate dimension"):
            worker._validate_output(duplicate)

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
                "thoughtsTokenCount": 7,
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
        self.assertEqual(
            config["thinkingConfig"],
            {"thinkingLevel": worker.DEFAULT_THINKING_LEVEL},
        )
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
        basis_schema = config["responseSchema"]["properties"]["dimension_basis"]
        self.assertEqual(
            set(basis_schema["items"]["properties"]["field"]["enum"]),
            set(worker.DIMENSION_BASIS_PATHS),
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
        self.assertEqual(config["maxOutputTokens"], 2048)
        self.assertEqual(usage["total_tokens"], 80)
        self.assertEqual(usage["thinking_tokens"], 7)
        self.assertEqual(worker._validate_output(result)["status"], "draft_ready")


if __name__ == "__main__":
    unittest.main()
