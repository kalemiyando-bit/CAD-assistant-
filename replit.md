# CAD Assistant

An engineering design assistant that coordinates AI work across CAD, technical drawings, PCB design, and related engineering software.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string

## Agent system

- Start a new engineering-design request with `.agents/skills/engineering-design-coordinator/SKILL.md`.
- Use the relevant discipline Skill: `mechanical-cad`, `2d-engineering-drawings`, or `pcb-design`.
- Use `independent-engineering-review` for a separate, read-only review.
- Shared assignment, design-contract, change-request, and review templates live under `.agents/skills/engineering-design-coordinator/references/`.
- The coordinator must ask which software the user is using and the desired research scope when those are not already stated.
- Agents own separate outputs. A reviewer reports findings and does not silently edit another agent's files.
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

## Architecture decisions

- The first version is conversational and Skill-driven; do not build a user-facing UI before validating the workflow.
- Ask for the target software and version per design task; do not claim direct access to desktop CAD/EDA software unless it is actually connected.
- Use bounded specialist roles, single-writer ownership, formal change requests, independent review, and deterministic checks where available.
- STEP is for 3D neutral geometry; dimensioned 2D drawings and circuit-board deliverables need their own formats.
- A release manifest detects missing, empty, or changed files; it does not prove engineering correctness.

## Product

The assistant helps the user develop their own engineering designs across SolidWorks, AutoCAD, and other CAD/EDA tools. It asks which software is being used, follows the research scope chosen for that task, and distinguishes verified information from assumptions and unvalidated design proposals.

## User preferences

- Ask which design software the user is using for each task; ask for version/OS when relevant.
- Ask each time how broad external research should be. Engineering rigor applies regardless of research scope.
- The user is building an engineering-support system, not seeking to copy a product's appearance.
- For robot 3D CAD handoffs, use STEP and keep the model coordinates Z-up, X length, and Y width.

## Gotchas

- The Robot V1 geometry is preliminary; packaging envelopes and approximate gear geometry are not manufacturing validation.
- A STEP file carries neutral 3D geometry but does not preserve a native SolidWorks feature tree.
- The default system Python currently cannot import CadQuery or ezdxf. Check the project environment before running the CAD generator; do not assume these tools are available or install packages without following package-management guidance.
- An AI or simulation “pass” is not proof of safe operation; retain failed checks and unverified values in the handoff.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
- See `DESIGN_AGENT_SYSTEM_CHARTER.md` for the agent-system contract and its current scope
