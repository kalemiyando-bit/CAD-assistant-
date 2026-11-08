---
name: Gemini REST schema quirks
description: Runtime constraints found when sending structured output schemas to Gemini's direct REST API.
---

For the direct Gemini `generateContent` REST API, do not assume a generic JSON Schema object can be passed unchanged as `generationConfig.responseSchema`. Live requests in this project rejected lower-case type names, a numeric enum value, and `additionalProperties`. The local worker now converts type names, omits the unsupported fields, and still performs strict shape/dimension validation before writing a model spec. That latest schema has not yet passed a live request.

The user prefers a slower, conservative Gemini workflow over the fastest response when that helps avoid hitting quotas.

On 2026-11-08, the user shared a Free-tier AI Studio snapshot for Gemini 3.8 Flash: limits of 5 RPM, 250,000 input TPM, and 20 RPD; 28-day peak use of 1 RPM, 568 TPM, and 3 RPD. Treat this as a dated observation, not a permanent quota.

**Why:** Provider schema incompatibilities and temporary high demand appeared only in live requests; the user wants to conserve quota and avoid frequent calls.

**How to apply:** Keep the provider schema within the API's accepted subset and enforce exact geometry rules locally. A successful provider response is not a validated CAD spec until the local validator accepts it. Keep calls sequential, output bounded, and automatic retries disabled; check project-specific limits and usage before retrying a timeout. Obtain user approval before a live request because it uses the user's separate Google billing.
