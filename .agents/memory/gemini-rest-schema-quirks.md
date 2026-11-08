---
name: Gemini REST schema quirks
description: Runtime constraints found when sending structured output schemas to Gemini's direct REST API.
---

For the direct Gemini `generateContent` REST API, do not assume a generic JSON Schema object can be passed unchanged as `generationConfig.responseSchema`. Earlier requests rejected lower-case type names, a numeric enum value, and `additionalProperties`; a later candidate response confirms the converted schema is accepted. Gemini 3.8 counts thought tokens against `maxOutputTokens`, so a small cap can truncate even a short structured answer. Its `minimal` thinking level is unsupported; use `low` for this bounded primitive-spec task and retain strict local validation.

The user prefers a slower, conservative Gemini workflow over the fastest response when that helps avoid hitting quotas.

On 2026-11-08, the user shared a Free-tier AI Studio snapshot for Gemini 3.8 Flash: limits of 5 RPM, 250,000 input TPM, and 20 RPD; 28-day peak use of 1 RPM, 568 TPM, and 3 RPD. Treat this as a dated observation, not a permanent quota.

The worker's current default is Gemini 3.6 Flash. On 2026-11-08, one primary-key live call for each supported shape (box, cylinder, annular cylinder, and plate with centered bore) passed strict local validation with exact requested dimensions and dimension provenance. This confirms one response per shape, not repeated reliability or Fusion/manufacturing validity.

The user confirms the three Gemini keys belong to different Google projects and wants the secondary keys used as quota backups. Gemini limits are per project, not per API key; try keys sequentially after HTTP 429 quota responses, but never retry the same key or fall back after HTTP 503/timeouts.

**Why:** Direct API schema restrictions and temporary capacity errors surfaced only in live requests. The user wants conservative quota use but has explicitly authorized billable Gemini calls for this project and asked the agent to choose the key strategy.

**How to apply:** Enforce exact geometry rules locally; a provider response is not a validated CAD spec until accepted by the local validator. Keep calls sequential and output bounded. Try configured keys serially after a clear invalid-key response or HTTP 429 project-quota response; do not retry the same key, parallelize requests, or fall back after an ambiguous timeout or HTTP 503 provider-capacity error. Use Gemini 3.6 Flash as the current default, but do not claim repeated reliability or CAD/manufacturing validity from the one-call-per-shape checks. Use `low` thinking for the bounded primitive-spec task; Gemini 3.8 counts thought tokens against its output cap and does not support `minimal`.
