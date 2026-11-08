# AI Compute Supplement for CAD Assistant

**Status:** The user agreed to a Replit-Agent-manager / Gemini-worker process. Replit Agent prepares a focused prompt or task file, the user returns Gemini's work for review, and Replit Agent issues revisions or takes over if Gemini cannot meet the requirements. The user's preferred Gemini API credential is their own key in Replit Secrets if direct API integration is implemented. No key, worker, or interface has been configured or built.

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
2. Replit Agent creates a focused prompt or task file for Gemini using only the context needed for that assignment.
3. Gemini performs the assigned work. The user returns its outputs to Replit Agent.
4. Replit Agent checks the result against the agreed requirements and prepares a focused follow-up prompt/file when changes are needed.
5. If Gemini cannot produce an acceptable result, Replit Agent takes over.

The shaft is a tested workflow example, not the system's design scope. Keep assignments bounded and do not give a model unrestricted project or file access by default. A prompt/file handoff is the agreed workflow; direct Gemini API automation and a user-facing interface have not been built. If direct API integration is later implemented, keep the user's credential in Replit Secrets and server-side only. A passing model response or a file that opens is not evidence of fit, strength, safety, or manufacturing readiness.

## Recommended first pilot

Use the tested shaft workflow as a small end-to-end Gemini pilot:

1. Replit Agent gathers the required design intent, software target, units, and 2D output purpose, then creates or confirms the design contract.
2. Gemini converts that approved brief into a strict, single-part specification with explicit assumptions and unknowns. It does not generate arbitrary executable code.
3. A deterministic adapter maps the specification to the existing 2D drawing input and Fusion model-spec input. Validate the result before generation and check that shared dimensions agree across both outputs.
4. Run the existing drawing/model tests and produce the normal handoff for user review in Fusion. Keep the outputs labeled preliminary.

This is more useful than a free-form chatbot pilot: it exercises the real brief-to-deliverable path, reuses the 2D and 3D shaft work already reported as passing, and measures whether Gemini saves Agent effort. The narrow schema, existing validators, and limited one-part scope keep the cost and failure modes easier to control. Only after this passes should the worker expand to more complex CAD scripting.

## Interface and automation scope

The initial agreed workflow is Replit-Agent-led with a prompt/task-file handoff and the user returning Gemini's result. The project charter prioritizes proving this process before building a user-facing interface. Whether to automate the Gemini call directly or add a workbench remains open; do not build either without a specific implementation request.

## Context and test-cost preferences

- Start with the project's `replit.md`, then read only the current task's contract, source files, and relevant Skill. Do not perform a broad repository review or repeat the full system summary for each task.
- Do not run full test suites routinely. For generated CAD files, first let the user check the output in the target CAD application. If it fails to load/import, use focused diagnostics and tests for that failure. Follow task-specific safety or release checks recorded in the design contract.
- Keep engineering claims evidence-based even when reducing routine test runs. Successful loading does not establish dimensional correctness, fit, strength, safety, or manufacturing readiness.

## Decisions to make before implementation

- Should the agreed prompt/file workflow be automated through the Gemini API, or remain user-mediated?
- Which actual design task should be the first worker assignment? The shaft may be reused as a test case but is not the product scope.
- What per-task cost ceiling and usage reporting should the pilot have?
- Which exact shaft-example tests passed, and did the 3D path run in Fusion and produce an archive that was opened and checked? Record the Fusion version and checks before updating the detailed evidence status.

No key or provider integration has been configured. When implementation is approved, add the user's Gemini credential through the project Secrets flow; never request it in chat or put it in source files.
