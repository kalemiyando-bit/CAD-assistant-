# Gemini Part-Spec Worker

## Purpose

This is the first bounded Gemini integration for CAD Assistant. Replit Agent
agrees the task with the user, prepares a focused input file, and invokes the
worker. Gemini returns a preliminary one-part model specification; the existing
Fusion validator checks it before the user chooses whether to continue.

This first worker accepts simple geometry supported by the Fusion v1 generator:
boxes, cylinders, annular cylinders, and plates with a centered bore. It is not
limited to shafts, but it does not yet produce assemblies, 2D drawings, arbitrary
CAD scripts, or manufacturing-ready designs.

## Current verification status

The local dry run and focused mocked API-contract checks pass. Live generation
is still unverified: one provider response was rejected by the worker's
exact-dimension check, and two later requests timed out (at 60 and 180 seconds).
The provider schema has since been corrected to omit the unsupported
`additionalProperties` field; the worker still validates exact dimensions
locally. Timeouts returned no usage metadata and may not prove the provider did
no work. No valid model-spec file or Fusion output has been produced by Gemini
yet. Check project usage in AI Studio before retrying; do not run unrelated CAD
test suites for this issue.

## Security and cost boundaries

- Run the worker from the trusted Replit project environment. It is a local CLI,
  not a public HTTP endpoint, so an unauthenticated caller cannot spend the
  user's Google API quota.
- `GEMINI_API_KEY` is read from Replit Secrets by the Python process. Never put
  the key in an input file, command argument, output file, or log.
- Only the three fields below are sent to Google: `design_name`,
  `design_brief`, and `approved_assumptions`. The worker does not read other
  project files, skills, or secrets.
- Each invocation makes at most one Google request, with a 180-second timeout,
  no automatic retries, and a 1,024-token output cap. It reports input, output,
  thinking, and total token usage
  when Google returns it. Google bills these API calls separately from Replit
  Agent usage.
- Gemini rate limits are project-level and can include requests per minute,
  input tokens per minute, and requests per day. They vary by model and usage
  tier; check the active project limits in [Google AI Studio](https://aistudio.google.com/rate-limit?timeRange=last-28-days).
  To keep this workflow conservative, run one worker at a time and review each
  result before starting another request.
- The worker never executes model-generated code. A valid result is only a
  preliminary geometry specification, not evidence of fit, strength, safety,
  or manufacturing readiness.

## Input

Create a JSON file for the approved design. Convert all dimensions to
millimetres before submission and include only assumptions the user has
approved.

```json
{
  "design_name": "Example Part A0",
  "design_brief": "Describe the single part and its explicitly supplied dimensions here.",
  "approved_assumptions": []
}
```

`design_name` may be omitted. `design_brief` is required and limited to 8,000
characters. `approved_assumptions` is optional, with at most 50 entries.

## Run

Validate the input without making a billable provider call:

```sh
python3 Project_files_being_worked_on/fusion_native_pilot/gemini_part_spec_worker.py \
  --input path/to/request.json \
  --dry-run
```

Generate and validate a draft, writing a new model-spec file only when the
result is ready:

```sh
python3 Project_files_being_worked_on/fusion_native_pilot/gemini_part_spec_worker.py \
  --input path/to/request.json \
  --output path/to/new_model_spec.json
```

The worker refuses to overwrite an existing output. If dimensions are missing,
it returns `needs_clarification` and questions without writing geometry. If the
part cannot be represented by one supported primitive, it returns
`unsupported`. A ready model spec is normalized by
`fusion_model_spec.validate_model_spec` before it is written.

The default model is `gemini-3.8-flash`; set `GEMINI_MODEL` or pass `--model` to
select another Google-enabled model. A dry run validates input and reports what
would be sent but does not verify the API key or contact Google.

## Handoff

Review the returned summary, assumptions, dimension sources, and token counts.
Only a `draft_ready` result includes a validated `model_spec`. The existing
Fusion script can use that JSON, but running the Fusion script, checking the
result in Autodesk Fusion, and producing 2D documentation remain separate
steps. Do not call a successful schema validation a Fusion import or engineering
validation.
