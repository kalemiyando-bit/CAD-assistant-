# AI Compute Supplement for CAD Assistant

**Status:** Discussion only. No provider, API key, integration, or application architecture has been selected or set up.

## User-reported workflow milestone

On 2026-11-08, the user reported that the tests passed and the shaft example demonstrates creation of both a 2D drawing and a 3D model. The engineering playbook records the related files and earlier checks; the exact tests and Fusion-side checks included in this latest confirmation are not yet itemized there. Read the playbook's more specific evidence notes before making claims about a particular import, archive, dimension check, or manufacturing readiness.

## The token and billing distinction

Replit Agent usage and a Gemini API call from an application are separate. Providing a Google API key to an application does not increase Replit Agent's own usage allowance. It can, however, move a well-defined, repeatable part of the workflow to a Gemini call so the Replit Agent is not asked to do every generation or analysis step itself.

There are two possible Gemini billing routes:

1. **Use a Google Gemini API key.** The app's server calls Gemini; store the key in Replit Secrets and keep it on the server, never in browser code or Git. Google bills the API usage directly.
2. **Use Replit AI Integrations.** Replit manages the provider credential, so no personal API key is needed. Gemini API usage is billed to Replit credits at the provider's public API rates and is tracked for the app.

Replit's documentation distinguishes Agent usage from AI API integration usage. The managed integration is convenient, but it does not meet the goal of moving inference charges away from Replit credits. If that separation is the priority, direct Google billing is the route to evaluate.

References:

- [Replit AI billing](https://docs.replit.com/billing/ai-billing)
- [Replit AI Integrations](https://docs.replit.com/features/integrations/replit-ai-integrations)
- [Replit Secrets](https://docs.replit.com/core-concepts/project-editor/app-setup/secrets)
- Project Gemini integration guidance: `.local/skills/ai-integrations-gemini/SKILL.md`

## A possible division of work

This is a proposal to discuss, not an approved change to the project's agent-first approach:

1. The user and Replit Agent establish the design contract, target CAD software, research scope, units, assumptions, and intended outputs.
2. A small, server-side Gemini worker receives only the relevant contract, selected Skill guidance, and approved input files. It returns a constrained result such as a model-specification draft or a CAD-script draft.
3. Existing deterministic generators and validators create/check the output. Replit Agent can use the project's Skills and files to coordinate the work, interpret failures, and review results.
4. The user reviews the package and runs Fusion-native scripts inside Autodesk Fusion when required. Gemini does not automatically have access to Replit project files, Skills, or Agent tools; a deliberate, permission-limited bridge would be needed to provide context or actions.

Start by offloading one bounded, repeatable step, not by giving a model unrestricted shell or file access. A structured model specification is a safer first target than letting an LLM directly overwrite CAD source or final deliverables. Keep deterministic checks and human engineering review; a passing script or model response is not evidence of fit, strength, safety, or manufacturing readiness.

## Minimal platform question

The project charter currently prioritizes proving conversational engineering workflows before building a user-facing interface. A minimal workbench could be considered later, but it should initially be limited to submitting a design task, viewing status and costs, inspecting generated files, and approving or rejecting changes. Whether this should be a small interface or remain Replit Agent-led is still open.

## Decisions to make before implementation

- Should Gemini usage be billed directly by Google through a key in Replit Secrets, or billed through Replit credits?
- Which single task should Gemini handle first: turning an approved brief into a structured model spec, drafting a CAD helper script, or reviewing generated files?
- Should the first version remain in the Replit Agent workflow, or include a minimal user-facing workbench?
- Which exact shaft-example tests passed, and did the 3D path run in Fusion and produce an archive that was opened and checked? Record the Fusion version and checks before updating the detailed evidence status.

No provider integration or credential has been configured as part of this discussion.
