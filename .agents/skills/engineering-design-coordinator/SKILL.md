---
name: engineering-design-coordinator
description: Starts and coordinates engineering design tasks from a brief, sketch, image, or existing model across CAD, technical drawings, and PCB workflows. Use when planning or coordinating a new engineering design.
---

# Engineering Design Coordinator

Own the user's design intent, the task contract, assignments, integration, and final handoff. This Skill coordinates specialist workflows; it does not replace discipline-specific engineering or validation.

## Start with the user's intent

Read `DESIGN_AGENT_SYSTEM_CHARTER.md` and the matching discipline Skill before substantive work. Do not repeat questions already answered in the user's brief, project files, or current conversation.

Before design work, establish:

1. What the design must do, where it will operate, and its important constraints.
2. **Which software the user is using**, and its version/operating system if compatibility or instructions depend on them. Distinguish the user's target software from tools actually available to the agent.
3. The requested deliverables and file formats.
4. The research scope for this task.
5. Critical unknowns that could change geometry, interfaces, safety, or cost.

If required details are missing, use the available question interface to ask a short, focused question. A sketch or photo can show intent, but it is not a scaled drawing without reliable dimensions or a scale reference.

## Research scope: ask each time unless explicit

Record one scope in the design contract:

- **Broad engineering and reference research:** existing products/mechanisms, supplier information, standards, and technical sources may be searched.
- **Engineering facts only:** research technical properties and constraints; do not search for similar products or use them as design templates.
- **User sources only:** use the user's supplied material; do not browse for more.
- **No external research:** do not browse; mark unsupported assumptions and unknowns.

If the user has not chosen and has not already described the scope, ask. A novel concept does not automatically prohibit searches. If the selected scope prevents checking a critical engineering fact, disclose the gap and ask before broadening research. Cite sources for sourced values; keep sourced facts separate from calculations, recommendations, and assumptions.

## Create the contract

Use `references/design-contract.md`. Keep requirements traceable and label values as user-provided, sourced, calculated, preliminary, supplier-dependent, assumed, or requiring test. Do not invent dimensions, ratings, or product specifications.

## Route work by discipline

Read only the needed Skills:

- Mechanical parts or assemblies: `../mechanical-cad/SKILL.md`
- Dimensioned drawings or 2D CAD: `../2d-engineering-drawings/SKILL.md`
- Circuit boards: `../pcb-design/SKILL.md`
- Independent review: `../independent-engineering-review/SKILL.md`

Use bounded specialist agents only when they can work independently. Assign one writer per source area or release output. Send assignments using `references/agent-handoff.md`; agents do not edit another owner's files. Cross-discipline findings become change requests using `references/change-request.md`.

When a separate subagent/reviewer cannot be used, perform a distinct review pass and clearly mark that it was not independent. Never describe a single-agent self-check as an independent review.

## Tool readiness and software handoff

Before substantial modeling or simulation, smoke-test every required tool path with a small, non-destructive known example. Check the actual exported/imported result, not just a successful command exit. If the target application is unavailable, say so and offer a compatible file, script/macro, or user-run instructions instead. Never imply that Replit can operate the user's local SolidWorks, AutoCAD, or EDA installation without a working connection.

Follow the target application's supported format and version. Ask before installing dependencies or invoking paid services. Stop on permission or access errors; do not bypass them.

## Repository and GitHub portability

- Never create, edit, delete, rename, or otherwise change any `.gitignore` file. If a required system file is ignored or untracked, stop and ask the user to resolve it.
- Keep project-owned source, Skills, references, scripts, tests, required assets, Replit configuration, dependency manifests, and lockfiles tracked so they can be transferred through GitHub.
- Track declarations and lockfiles, not installed copies such as `node_modules` or runtime caches. A fresh Replit must be able to recreate dependencies from the tracked package files.
- Before claiming a handoff is portable, check that its required files are tracked and are not excluded by ignore rules.

## Review and release

Use the independent review Skill and `references/review-report.md`. Recompute reported metrics from source data where practical. Do not tune criteria, omit failed checks, or replace a failed result with a better-looking visualization.

Before handoff:

- Check the actual files against the requested deliverables and target software.
- Run the relevant geometry, dimensional, import, drawing, or electrical checks that are available.
- Include a concise manifest, revision, units, coordinate frame, evidence, limitations, and next steps.
- Use `scripts/release_manifest.py` to create or verify a file/hash manifest for a release folder.
- Preserve a release once issued. Fixes become a new revision or addendum; do not silently rewrite the prior release.
- Do not claim certification, safety, manufacturing readiness, or physical performance without the required evidence.

