# AI Compute Supplement for CAD Assistant

**Status:** The user approved direct Gemini API use with their own key in Replit Secrets. A local CLI worker drafts a single-component Fusion v1 model specification from an explicitly supplied brief and validates it with the existing Python validator. It makes no public billable endpoint and has no UI. The no-cost dry run and focused mocked API-contract checks pass. Live generation is not yet verified: one provider response failed local dimension validation, and after fixing the REST schema, two requests timed out (at 60 and 180 seconds). Timeouts returned no usage metadata and may not prove the provider did no work. No valid model-spec file or Fusion output was produced.

The system supports the user's broader engineering design work; the shaft is only a workflow test example. Do not design only for shafts.

## User-reported workflow milestone

On 2026-11-08, the user reported that the tests passed and the shaft example demonstrates creation of both a 2D drawing and a 3D model. The engineering playbook records the related files and earlier checks; the exact tests and Fusion-side checks included in this latest confirmation are not yet itemized there. Read the playbook's more specific evidence notes before making claims about a particular import, archive, dimension check, or manufacturing readiness.

## The token and billing distinction

Replit Agent usage and a Gemini API call from an application are separate. Providing a Google API key to an application does not increase Replit Agent's own usage allowance. It can, however, move a well-defined, repeatable part of the workflow to a Gemini call so the Replit Agent is not asked to do every generation or analysis step itself.

There are two possible Gemini billing routes:

1. **Use a Google Gemini API key — user's stated preference.** The app's server calls Gemini; store the key in Replit Secrets and keep it on the server, never in browser code or Git. Google bills the API usage directly.
2. **Use Replit AI Integrations.** Replit manages the provider credential, so no personal API key is needed. Gemini API usage is billed to Replit credits at the provider's public API rates and is tracked for the app.

Replit's documentation distinguishes Agent usage from AI API integration usage. The managed integration is convenient, but it does not meet the goal of moving inference charges away from Replit credits. Direct Google billing is the route to use unless the user later changes this preference.

References:

- [Replit AI billing](https://docs.replit.com/billing/ai-billing)
- [Replit AI Integrations](https://docs.replit.com/features/integrations/replit-ai-integrations)
- [Replit Secrets](https://docs.replit.com/core-concepts/project-editor/app-setup/secrets)
- Project Gemini integration guidance: `.local/skills/ai-integrations-gemini/SKILL.md`

## Agreed division of work

The user approved this operating model:

1. The user and Replit Agent agree on the task, requirements, target CAD software, research scope, assumptions, and intended outputs.
2. Replit Agent prepares a focused JSON brief and invokes the local Gemini worker only for supported single-part Fusion geometry.
3. Gemini returns a structured draft; the worker validates it against the existing Fusion v1 model-spec validator. It never executes model-generated code.
4. Replit Agent checks the result against the agreed requirements, presents the draft for user review, and prepares a focused revision request when needed.
5. If Gemini cannot produce an acceptable result, Replit Agent takes over. Fusion execution and user inspection remain separate steps.

The shaft is a tested workflow example, not the system's design scope. Keep assignments bounded and do not give a model unrestricted project or file access. The local CLI reads only its input JSON, returns a preliminary spec, and does not create a 2D drawing or Fusion archive. A passing model response or a file that opens is not evidence of fit, strength, safety, or manufacturing readiness.

## Recommended first pilot

Use the tested shaft workflow as a small end-to-end Gemini pilot:

1. Replit Agent gathers the required design intent, software target, units, and 2D output purpose, then creates or confirms the design contract.
2. Gemini converts that approved brief into a strict, single-part specification with explicit assumptions and unknowns. It does not generate arbitrary executable code.
3. A deterministic adapter maps the specification to the existing 2D drawing input and Fusion model-spec input. Validate the result before generation and check that shared dimensions agree across both outputs.
4. Run the existing drawing/model tests and produce the normal handoff for user review in Fusion. Keep the outputs labeled preliminary.

This is more useful than a free-form chatbot pilot: it exercises the real brief-to-deliverable path, reuses the 2D and 3D shaft work already reported as passing, and measures whether Gemini saves Agent effort. The narrow schema, existing validators, and limited one-part scope keep the cost and failure modes easier to control. Only after this passes should the worker expand to more complex CAD scripting.

## Interface and automation scope

The Gemini call is now automated through the local CLI, but the overall process remains Replit-Agent-led and user-reviewed. There is no user-facing interface or public API route. Keep it this way unless repeated real use demonstrates a need for one.

## Context and test-cost preferences

- Start with the project's `replit.md`, then read only the current task's contract, source files, and relevant Skill. Do not perform a broad repository review or repeat the full system summary for each task.
- Do not run full test suites routinely. For generated CAD files, first let the user check the output in the target CAD application. If it fails to load/import, use focused diagnostics and tests for that failure. Follow task-specific safety or release checks recorded in the design contract.
- Keep engineering claims evidence-based even when reducing routine test runs. Successful loading does not establish dimensional correctness, fit, strength, safety, or manufacturing readiness.

## Remaining pilot decisions and checks

- What per-task cost ceiling and usage reporting should the pilot have?
- Which real design task should follow the bounded smoke test? The shaft may be reused as a test case but is not the product scope.
- Should the next integration step map a validated model spec into both the existing 2D and Fusion paths? The current worker only returns the Fusion v1 spec.
- Which exact shaft-example tests passed, and did the 3D path run in Fusion and produce an archive that was opened and checked? Record the Fusion version and checks before updating the detailed evidence status.

The current project has a `GEMINI_API_KEY` secret configured. Never request or print its value in chat, logs, or source files. Google applies RPM, input TPM, and RPD quotas per project; active limits vary by model and usage tier and must be checked in Google AI Studio. Check the project's actual usage there before retrying after a timeout.
