# CAD Assistant

An engineering design assistant that coordinates AI work across CAD, technical drawings, PCB design, and related engineering software.

## Start Here

- For every new design request, read `DESIGN_TASK_START_HERE.md` first and follow its focused intake and execution steps.
- Keep work focused on the user's current design request. Read only its brief/contract, directly relevant files, and matching Skill; do not scan or summarize the whole repository unless asked or necessary.
- `DESIGN_AGENT_SYSTEM_CHARTER.md` holds cross-project engineering principles.
- `ENGINEERING_WORKFLOW_PLAYBOOK.md` documents existing generation paths and their evidence status.
- `AI_COMPUTE_SUPPLEMENT_DISCUSSION.md` records the agreed Gemini handoff.
- `GEMINI_WORKER.md` explains the bounded Gemini CLI workflow and input format.
- The shaft is a workflow example, not the system's design scope.
- Replit Agent manages the design task and prepares focused prompts/files for Gemini. The user returns results for review; Replit Agent issues revisions or takes over if Gemini cannot meet the requirements.
- Avoid broad context reviews and repeated project summaries. Do not run full test suites routinely; for CAD outputs, first check loading in the target application and use focused diagnostics if it fails. Keep contract-required safety/release checks.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Agent system

- Use `DESIGN_TASK_START_HERE.md` to begin each new design request without a broad repository review.
- Start a new engineering-design request with `.agents/skills/engineering-design-coordinator/SKILL.md`.
- Read `ENGINEERING_WORKFLOW_PLAYBOOK.md` for project-specific generation paths and which CAD/EDA checks have or have not passed.
- Use the relevant discipline Skill: `mechanical-cad`, `2d-engineering-drawings`, or `pcb-design`.
- Use `independent-engineering-review` for a separate, read-only review.
- Shared assignment, design-contract, change-request, and review templates live under `.agents/skills/engineering-design-coordinator/references/`.
- The coordinator must ask which software the user is using and the desired research scope when those are not already stated.
- Autodesk Fusion is the planned primary CAD target, but continue asking which software is intended for each design task.
- Agents own separate outputs. A reviewer reports findings and does not silently edit another agent's files.
- No agent may create, edit, delete, rename, or otherwise change `.gitignore`. Keep required project source, Skills, assets, Replit configuration, dependency manifests, and lockfiles tracked for GitHub transfer; if a required file is ignored or untracked, stop and ask the user.
- Track dependency manifests and lockfiles, not installed folders such as `node_modules` or temporary caches; dependencies must be reproducible in a fresh Replit.
- No user-facing design-system interface is in scope until the conversational workflows are proven.

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `.agents/skills/` — reusable engineering workflow and role guidance
- `DESIGN_AGENT_SYSTEM_CHARTER.md` — system principles, gates, and proposed output conventions
- `Project_files_being_worked_on/ROBOT_V1_DESIGN/` — preliminary robot design brief and CadQuery source used as a future mechanical pilot
- `.agents/skills/engineering-design-coordinator/scripts/release_manifest.py` — standard-library release file/hash manifest tool
- `Project_files_being_worked_on/fusion_native_pilot/` — Fusion scripts and the tested-outside-Fusion model-spec validator
- `Project_files_being_worked_on/wheel_drive_bench_demo/` — preliminary wheel-drive concept, assumptions, and model specification
- `ENGINEERING_WORKFLOW_PLAYBOOK.md` — reproducible 2D/3D/PCB handoff paths and evidence status
- `AI_COMPUTE_SUPPLEMENT_DISCUSSION.md` — agreed Gemini handoff process, credential handling, and unresolved automation decisions

## Architecture decisions

- This is an agent-support system for the user and other Replit agents to help build CAD designs, not a web app or standalone Python app. Keep it conversational and Skill-driven; Python may be used for helper scripts, but not as the product. Do not build user-facing UI before validating the workflow.
- Ask for the target software and version per design task; do not claim direct access to desktop CAD/EDA software unless it is actually connected.
- Use bounded specialist roles, single-writer ownership, formal change requests, independent review, and deterministic checks where available.
- Prefer native Fusion `.f3d`/`.f3z` output when Fusion is the target and the design can be created or exported through Fusion. STEP is the neutral 3D fallback; imported STEP does not restore the original feature history. Dimensioned 2D drawings and circuit-board deliverables need their own formats.
- A release manifest detects missing, empty, or changed files; it does not prove engineering correctness.
- Gemini is an optional local CLI worker for preliminary single-part Fusion specs. It reads `GEMINI_API_KEY` and its numbered fallbacks from Replit Secrets, has no public route or UI, and must not receive unapproved assumptions or execute generated code. See `GEMINI_WORKER.md`.

## Product

The assistant helps the user develop their own engineering designs across Autodesk Fusion, SolidWorks, AutoCAD, and other CAD/EDA tools. Fusion is the planned primary CAD target, but the assistant asks which software is being used for each task, follows the selected research scope, and distinguishes verified information from assumptions and unvalidated design proposals.

## User preferences

- Ask which design software the user is using for each task; ask for version/OS when relevant.
- Ask each time how broad external research should be. Engineering rigor applies regardless of research scope.
- The user is building an engineering-support system, not seeking to copy a product's appearance.
- For robot 3D CAD handoffs, prefer native Fusion archives when Fusion is the target and can produce them; use STEP for neutral exchange or when requested. Keep robot model coordinates Z-up, X length, and Y width.

## Gotchas

- The Robot V1 geometry is preliminary; packaging envelopes and approximate gear geometry are not manufacturing validation.
- A STEP file carries neutral 3D geometry but does not preserve the source CAD application's parametric feature history.
- The default system Python currently cannot import CadQuery or ezdxf. Check the project environment before running the CAD generator; do not assume these tools are available or install packages without following package-management guidance.
- An AI or simulation “pass” is not proof of safe operation; retain failed checks and unverified values in the handoff.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
- See `DESIGN_AGENT_SYSTEM_CHARTER.md` for the agent-system contract and its current scope
