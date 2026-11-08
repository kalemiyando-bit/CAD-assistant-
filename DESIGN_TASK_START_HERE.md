# Start Here for a Design Task

Use this guide at the start of each new engineering design request. It is an
intake and execution guide for CAD Assistant, not a request to inspect the
entire repository.

## Prompt to start a task

The user can begin with:

> Read `DESIGN_TASK_START_HERE.md` first and follow it for this request. Ask only
> for missing design-critical information, and invite me to upload useful
> sketches, photos, drawings, or existing CAD files. Do not scan the whole
> repository. Once the brief is clear, follow the relevant design workflow and
> carry out the requested work.

## 1. Orient narrowly

- This project is a conversational engineering design assistant, not a
  conventional web app.
- Read `replit.md` for project rules and the file map. Do not scan every folder,
  read every Skill, repeat the project history, or run broad test suites.
- Before substantive design work, read
  `DESIGN_AGENT_SYSTEM_CHARTER.md`, the engineering design coordinator Skill,
  and only the discipline Skills and project files relevant to this request.
- Treat existing parts and example projects as workflow examples, not as
  requirements for the new design.

## 2. Establish the design intent

Do not ask questions the user has already answered in the conversation, brief,
or supplied files. Ask a short, focused set of questions, in stages if needed.
Cover the items that matter to this design:

- What the design must do, who will use it, and where it will operate.
- Which software the user will use; ask its version or operating system when
  that affects compatibility or instructions.
- The requested deliverables and formats. For 2D work, ask whether it is for
  creating 3D geometry, documentation, or both; keep the outputs separate.
- Known dimensions, units, coordinate frame, envelopes, mounting points,
  interfaces, loads, motion, electrical limits, safety needs, materials,
  manufacturing methods, available components, and constraints such as cost.
- The desired research scope, unless the user has already stated it:
  - Broad engineering and reference research.
  - Engineering facts only; do not search for similar products as templates.
  - User-supplied sources only.
  - No external research.

Ask only what is relevant. Do not turn every intake into a long questionnaire.
Resolve unknowns that could materially change geometry, interfaces, safety, or
cost before proceeding. For noncritical unknowns, state a reversible assumption
and continue.

## 3. Invite useful reference files

When visual or existing design material would clarify intent, ask the user
whether they have a sketch, photo, annotated drawing, reference file, or current
CAD/EDA model they can upload. Make uploads optional when the user can explain
the design without them. If a file is supplied, follow the
`reading-uploaded-files` Skill and any relevant discipline-specific file
guidance; inspect only what answers the current design questions.

Ask the user to identify important views, known dimensions, units, scale
references, and which details are requirements versus inspiration. A photo or
unscaled sketch can communicate shape and intent, but it is not a dimensioned
drawing. Never derive precise dimensions from appearance alone.

## 4. Record and execute the agreed task

Once the intent is clear, create a concise design contract using
`.agents/skills/engineering-design-coordinator/references/design-contract.md`.
Label information as user-provided, sourced, calculated, preliminary, assumed,
or requiring testing. Keep the requirements traceable to the requested outputs.

Then:

- Read the matching discipline Skill and follow its workflow.
- Use specialist agents only for bounded work that can be done independently;
  keep one writer per shared output. Independent reviewers remain read-only.
- Check that the required software or export path is available before
  substantial modeling. If it is not, offer a compatible file, script, or
  user-run instructions and state the limitation.
- Use the Gemini worker only for supported preliminary, single-part Fusion
  specifications. Its supported primitives and current evidence are recorded
  in `GEMINI_WORKER.md`; it does not create drawings or assemblies or certify a
  design. Do not send unapproved assumptions or execute model-generated code.
- When this project is imported into a new Replit, its Secrets are not copied
  with the files. If a task needs Gemini, check only whether the required secret
  names are present; if they are missing, tell the user to add them through that
  project's Secrets tool. Never request or print secret values in chat or files.
  Make a paid API call only when the user has authorized it for that project or
  task.
- Do not make paid API calls, start expensive simulations, or add dependencies
  unless the user has authorized them for this project or task.

## 5. Verify and hand off honestly

Check the actual requested files and run focused validations that apply to the
task. When the target application is unavailable, say which checks could not be
performed and provide the user with clear steps to inspect the result there.
Keep failed checks, assumptions, and unverified values visible.

Finish with a concise handoff listing the deliverables, units and coordinate
frame where relevant, checks performed, remaining questions, and limitations.
Do not describe a valid file, model response, or successful import as proof of
fit, strength, safety, compliance, or manufacturing readiness.
