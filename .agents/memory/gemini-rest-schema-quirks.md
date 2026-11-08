---
name: Gemini REST schema quirks
description: Runtime constraints found when sending structured output schemas to Gemini's direct REST API.
---

For the direct Gemini `generateContent` REST API, do not assume a generic JSON Schema object can be passed unchanged as `generationConfig.responseSchema`. Live requests in this project rejected lower-case type names, a numeric enum value, and `additionalProperties`. The local worker now converts type names, omits the unsupported fields, and still performs strict shape/dimension validation before writing a model spec. That latest schema has not yet passed a live request.

**Why:** These incompatibilities appeared only in provider responses; the offline mocked API test cannot validate Google's REST schema parser.

**How to apply:** Keep the provider schema within the API's accepted subset and enforce exact geometry rules locally. A successful provider response is not a validated CAD spec until the local validator accepts it. Obtain user approval before a live request because it uses the user's separate Google billing.
