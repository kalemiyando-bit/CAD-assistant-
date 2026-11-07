# Engineering Design Agent System Charter

**Status:** Conversational workflow foundation implemented; Fusion pilot awaiting execution in Autodesk Fusion  
**Purpose:** Define how AI agents help turn a user's design brief and references into reviewable engineering deliverables.

## 1. Mission

Build a flexible, Replit-first workflow that supports the user's own engineering designs across mechanical 3D CAD, 2D engineering drawings, circuit-board drafts, and relevant design software. The system should later be portable to other AI tools by keeping its core brief format, evidence rules, handoffs, and review checklists platform-neutral.

The system assists with engineering design; it is not a product-look replication workflow. It should make useful design work easier without implying that arbitrary designs are automatically correct, safe, certified, or ready to manufacture.

## 2. Operating principles

- The user owns the design intent, originality, research scope, and final decisions.
- Ask about research scope for each project when it has not already been specified. Do not assume that a novel concept forbids all research or that research is always wanted.
- Engineering rigor applies in every research mode. Distinguish sourced facts, calculations, user requirements, preliminary targets, assumptions, supplier-dependent values, and items requiring testing.
- Do not invent missing dimensions or component capabilities and present them as verified.
- Prefer a small, purposeful group of agents and tools. Add specialist roles only when the task needs them.
- Do not let the creator approve its own work as the sole quality check.
- Escalate critical ambiguities to the user; otherwise proceed with explicit, reversible assumptions.
- Keep the first version focused on agent workflows and reusable guidance. A user-facing interface is out of scope until the process has been proven.

## 3. Research choices

At the start of a design task, record one of these scopes:

1. **Broad engineering and reference research** — search for relevant existing products, mechanisms, suppliers, standards, and technical sources. Cite sources and state what was borrowed, adapted, or independently derived.
2. **Engineering facts only** — research materials, physical limits, standards, safety, and other technical questions, but do not search for similar products or use them as design templates.
3. **User sources only** — use the user's brief, attachments, and explicitly supplied references; do not browse for additional sources.
4. **No external research** — work from the supplied information and general reasoning. Clearly mark unsupported assumptions and unresolved questions.

The selected scope controls external research, not the standard of engineering review. If a needed safety or feasibility fact is unavailable within the selected scope, explain the limitation and ask whether the scope may be widened.

## 4. Project intake

Before design work, create a short design contract containing:

- Intended function, users, and operating environment
- Required dimensions, units, coordinate frame, and envelope
- Loads, speeds, electrical/mechanical constraints, and safety needs
- Materials, manufacturing methods, cost, and available components, when known
- User-provided requirements versus recommendations and open assumptions
- Attached sketches/images: visible features, inferred relationships, and missing scale or dimensions
- Design software the user is using, including version and operating system when relevant
- Chosen research scope
- Required deliverables and their formats
- Verification expected before handoff

Do not treat an image as a dimensioned drawing unless it includes a reliable scale or dimensions.

### Software selection

Ask at the start of each design task: **“Which software are you using for this work?”** Include relevant choices such as SolidWorks, AutoCAD, FreeCAD, Fusion, Onshape, KiCad, another named tool, or “not sure yet.” Ask for the version and operating system when they affect file compatibility or instructions.

Distinguish the user's editing software from the tool the agent can actually run. State whether the handoff is a native file, a neutral exchange file, a script or macro for the user's software, or step-by-step instructions. Never claim direct access to an application unless the current environment has a working connection to it.

### Tool readiness

Before substantial modeling or simulation, run a small, non-destructive smoke test for each required software/tool connection. Use a known simple operation and check its expected output—for example, create and export a basic solid, re-import it, or run a test calculation with a known result. If the test fails, report the blocker rather than building on an unverified tool path.

## 5. Roles and separation of duties

The coordinator is responsible for the overall task, the design contract, task assignments, integration, and the final handoff.

Depending on scope, the coordinator may assign:

- **Research role:** gathers only the sources allowed by the selected research scope and labels evidence.
- **Discipline designer:** develops the mechanical, drafting, or PCB work and records decisions and assumptions.
- **Independent reviewer:** checks the proposed result against the design contract and reports findings without silently changing requirements.
- **Deterministic validator:** runs CAD-kernel, geometry, dimensional, electrical-rule, design-rule, or file-integrity checks where tools are available.
- **Documentation role:** prepares the component list, dimension schedule, calculation notes, and target CAD/EDA handoff instructions.

These are task roles, not a requirement to launch a permanent agent swarm. A small task may use fewer roles, but independent review and automated checks should be used where practical.

### Ownership and change requests

Assign one writer/owner to each shared output, source folder, or subsystem at a time. Other agents must not overwrite or delete that work. If a specialist finds a problem in another specialist's design, it submits a change request to the coordinator with the evidence, affected interfaces, and proposed correction. The coordinator routes the change to the owner and tracks re-checks. Do not resolve conflicts by letting two agents write to the same outputs concurrently.

## 6. Design and review workflow

### Gate A — Brief agreed

The design contract, target software, research scope, output formats, and critical unknowns are recorded. Required tool smoke tests pass. Ask the user to resolve ambiguities that could materially change the design.

### Gate B — Architecture proposed

Present the main concept, alternatives when useful, key interfaces, and preliminary calculations. Keep the user's requested design intent distinct from the agent's recommendations.

### Gate C — Deliverables created

Generate the requested geometry, drawings, or board design from a consistent set of dimensions and interfaces. Keep source files and exports organized for repeatable revision.

### Gate D — Independent checks

Compare the result with the contract. Run available mechanical, dimensional, geometry, electrical, file, and import checks. Independently recompute important reported values from source data or scripts instead of trusting an agent's summary. For simulations, check relevant convergence/sensitivity, conservation or balance, and the actual quantity of interest; report when criteria are not met. Record every failed or unavailable check; do not hide failures behind a polished visualization.

### Gate E — Handoff

Deliver the requested files with a concise manifest, units, revision, coordinate frame, known limitations, check results, and next steps for editing or testing. Audit that every expected file exists, is non-empty, has the requested format, and can be opened or re-imported where tools permit. Tie outward-facing performance or safety claims to a requirement and its actual evidence.

## 7. Proposed deliverable conventions

These are proposed defaults to refine with the user:

- **3D mechanical parts and assemblies:** STEP for neutral solid geometry. For robot geometry, use millimetres and the agreed model axes: global Z vertical, X chassis length, and Y chassis width. STEP does not preserve the source CAD application's parametric feature history.
- **Autodesk Fusion handoff:** When Fusion is the target and Fusion itself or its API is available, prefer a native `.f3d` design archive; use `.f3z` for Fusion assembly archives where appropriate. Autodesk's export API must run inside Fusion. If geometry is generated outside Fusion, use STEP as the neutral handoff or provide a Fusion script for the user to run; importing STEP and saving as `.f3d` does not recreate the original parametric feature history.
- **2D engineering drawings:** PDF for readable sheets and DXF for editable 2D geometry. STEP describes 3D geometry; it is not a dimensioned 2D drawing sheet.
- **Circuit-board drafts:** an editable native EDA project, fabrication outputs such as Gerber and drill files when requested, and a STEP board/mechanical model when needed for enclosure fit.

Never label concept geometry or unverified board outputs as production-ready. Keep deliverables limited to the formats the user requested.

## 8. Verification and safety

Use deterministic checks where possible:

- 3D CAD: valid solids, expected units and extents, coordinate orientation, part/assembly structure, basic clearances, and STEP re-import.
- 2D drawings: agreement with the model and dimension schedule, units, scale, view consistency, file readability, and human legibility.
- PCB: schematic/netlist consistency and available electrical-rule and design-rule checks; note any missing manufacturer constraints and review the schematic for human readability.
- Visual review: inspect the actual geometry, assembly/service access, motion, drawing views, and schematic readability. A successful render or plausible image is not proof of correct geometry or fit; use views generated from the real model and label illustrative images as such.

For numerical simulations, check mesh/time-step sensitivity, conservation or balance, solver behavior, and whether the chosen output has stabilized. Recompute critical metrics independently when practical. A solver's “pass” label alone is not proof.

An agent review is not a substitute for physical testing or qualified engineering review. Do not claim regulatory compliance, certified safety, structural adequacy, or manufacturability without the required evidence. Mark simulated, calculated, estimated, and physically measured values distinctly.

## 9. Resource and release control

- Agree on time, compute, storage, and any paid-service limits before expensive simulations, renders, or external services.
- Keep a simple record of resource use for long or costly jobs. Do not silently delete files to make room; show the user what could be removed and wait for approval.
- Follow the chosen research scope for network access. Disclose required external services or dependencies, and stop rather than bypassing a permission, access, or service error.
- Before handoff, create a manifest of expected deliverables and their hashes so missing or changed files can be detected.
- Treat a released package as immutable. If something is missing or wrong afterward, issue a new revision or addendum and preserve the original release.

### Repository integrity and portability

- `.gitignore` is user-controlled. Agents must never create, edit, delete, rename, or otherwise change any `.gitignore` file. If a required file is ignored or cannot be tracked, stop and ask the user to resolve it; do not change ignore rules or use another location to bypass them.
- Keep project-owned files needed to reproduce the system in GitHub: source, engineering Skills and references, scripts and tests, required project assets, Replit configuration, dependency declarations, and lockfiles.
- Track dependency manifests and lockfiles (such as `package.json` with `pnpm-lock.yaml`, and `pyproject.toml` with `uv.lock` or a required `requirements.txt`). Do not commit installed dependency folders, caches, or disposable build output; a fresh Replit should recreate those from the tracked declarations and locks.
- Before a handoff or portability claim, verify required paths are tracked and not ignored. If a required file exists only in the current Replit runtime, report it as a portability blocker rather than claiming the project is transferable.

## 10. Replit implementation direction

- Store repeatable procedures as project Skills, with separate skills for intake/orchestration, mechanical CAD, 2D drafting, PCB work, and validation as each workflow is developed.
- Use Replit agents or subagents for bounded, independently reviewable assignments; the coordinator remains responsible for integration and user communication.
- Keep the shared design contract and evidence rules understandable outside Replit so the workflow can later be adapted to other AI systems.
- Build no user-facing app until repeated real tasks show that an interface would remove meaningful friction.

## 11. Pilot and success criteria

The existing Robot V1 brief and CAD source are a candidate mechanical pilot, not a correctness baseline: parts of that model are preliminary packaging envelopes and require engineering validation.

The pilot succeeds when the workflow can:

- Capture requirements and research scope without losing the user's intent
- Ask which design software the user uses and adapt the handoff to its real capabilities
- Keep dimensions, coordinate systems, and assumptions consistent
- Produce a useful Fusion handoff, preferring native archives where Fusion can create them and using STEP as a verified fallback
- Identify limitations and failed checks instead of overstating confidence
- Demonstrate that smoke tests, independent review, source-based audits, and deterministic checks catch issues

The first Fusion pilot now includes a validated JSON model specification, an in-Fusion native sketch/extrude generator for boxes and cylinders, and a STEP-to-F3D archive path with explicit feature-history limitations. Local tests cover only schema validation and Python syntax; the actual Fusion API smoke test remains outstanding.

After the Fusion pilot is run and reviewed in Autodesk Fusion, extend the workflow to 2D drawings and PCB drafts. Add other design disciplines only as concrete needs arise.
