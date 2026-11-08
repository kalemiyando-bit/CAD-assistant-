---
name: Gemini REST schema quirks
description: Runtime constraints found when sending structured output schemas to Gemini's direct REST API.
---

For the direct Gemini `generateContent` REST API, do not assume a generic JSON Schema object can be passed unchanged as `generationConfig.responseSchema`. Earlier requests rejected lower-case type names, a numeric enum value, and `additionalProperties`; a later candidate response confirms the converted schema is accepted. Gemini 3.8 counts thought tokens against `maxOutputTokens`, so a small cap can truncate even a short structured answer. Its `minimal` thinking level is unsupported; use `low` for this bounded primitive-spec task and retain strict local validation.

The user prefers a slower, conservative Gemini workflow over the fastest response when that helps avoid hitting quotas.

On 2026-11-08, the user shared a Free-tier AI Studio snapshot for Gemini 3.8 Flash: limits of 5 RPM, 250,000 input TPM, and 20 RPD; 28-day peak use of 1 RPM, 568 TPM, and 3 RPD. Treat this as a dated observation, not a permanent quota.

**Why:** Direct API schema restrictions and temporary capacity errors surfaced only in live requests. The user wants conservative quota use but has explicitly authorized billable Gemini calls for this project and asked the agent to choose the key strategy.

**How to apply:** Enforce exact geometry rules locally; a provider response is not a validated CAD spec until accepted by the local validator. Keep calls sequential, output bounded, and automatic retries disabled. Try configured keys serially only after a clear invalid-key response; never parallelize requests or retry ambiguous failures. Use `low` thinking for this narrow primitive-spec task because Gemini 3.8 counts thought tokens against its output cap; do not use its unsupported `minimal` level.
