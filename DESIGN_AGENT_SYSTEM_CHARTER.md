# Engineering Design Agent System Charter

**Status:** Draft for discussion  
**Purpose:** Define how AI agents help turn a user's design brief and references into reviewable engineering deliverables.

## 1. Mission

Build a flexible, Replit-first workflow that can support mechanical 3D CAD, 2D engineering drawings, and circuit-board drafts. The system should later be portable to other AI tools by keeping its core brief format, evidence rules, handoffs, and review checklists platform-neutral.

The system should make useful design work easier; it must not imply that arbitrary designs are automatically correct, safe, certified, or ready to manufacture.

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
- Chosen research scope
- Required deliverables and their formats
- Verification expected before handoff

Do not treat an image as a dimensioned drawing unless it includes a reliable scale or dimensions.

## 5. Roles and separation of duties

The coordinator is responsible for the overall task, the design contract, task assignments, integration, and the final handoff.

Depending on scope, the coordinator may assign:

- **Research role:** gathers only the sources allowed by the selected research scope and labels evidence.
- **Discipline designer:** develops the mechanical, drafting, or PCB work and records decisions and assumptions.
- **Independent reviewer:** checks the proposed result against the design contract and reports findings without silently changing requirements.
- **Deterministic validator:** runs CAD-kernel, geometry, dimensional, electrical-rule, design-rule, or file-integrity checks where tools are available.
- **Documentation role:** prepares the component list, dimension schedule, calculation notes, and SolidWorks or EDA handoff instructions.

These are task roles, not a requirement to launch a permanent agent swarm. A small task may use fewer roles, but independent review and automated checks should be used where practical.

## 6. Design and review workflow

### Gate A — Brief agreed

The design contract, research scope, output formats, and critical unknowns are recorded. Ask the user to resolve ambiguities that could materially change the design.

### Gate B — Architecture proposed

Present the main concept, alternatives when useful, key interfaces, and preliminary calculations. Keep the user's requested design intent distinct from the agent's recommendations.

### Gate C — Deliverables created

Generate the requested geometry, drawings, or board design from a consistent set of dimensions and interfaces. Keep source files and exports organized for repeatable revision.

### Gate D — Independent checks

Compare the result with the contract. Run available mechanical, dimensional, geometry, electrical, file, and import checks. Record every failed or unavailable check; do not hide failures behind a polished visualization.

### Gate E — Handoff

Deliver the requested files with a concise manifest, units, revision, coordinate frame, known limitations, check results, and next steps for editing or testing.

## 7. Proposed deliverable conventions

These are proposed defaults to refine with the user:

- **3D mechanical parts and assemblies:** STEP for neutral solid geometry. For robot geometry, use millimetres and the agreed model axes: global Z vertical, X chassis length, and Y chassis width. STEP does not preserve a native SolidWorks feature tree.
- **2D engineering drawings:** PDF for readable sheets and DXF for editable 2D geometry. STEP describes 3D geometry; it is not a dimensioned 2D drawing sheet.
- **Circuit-board drafts:** an editable native EDA project, fabrication outputs such as Gerber and drill files when requested, and a STEP board/mechanical model when needed for enclosure fit.

Never label concept geometry or unverified board outputs as production-ready. Keep deliverables limited to the formats the user requested.

## 8. Verification and safety

Use deterministic checks where possible:

- 3D CAD: valid solids, expected units and extents, coordinate orientation, part/assembly structure, basic clearances, and STEP re-import.
- 2D drawings: agreement with the model and dimension schedule, units, scale, view consistency, and file readability.
- PCB: schematic/netlist consistency and available electrical-rule and design-rule checks; note any missing manufacturer constraints.

An agent review is not a substitute for physical testing or qualified engineering review. Do not claim regulatory compliance, certified safety, structural adequacy, or manufacturability without the required evidence.

## 9. Replit implementation direction

- Store repeatable procedures as project Skills, with separate skills for intake/orchestration, mechanical CAD, 2D drafting, PCB work, and validation as each workflow is developed.
- Use Replit agents or subagents for bounded, independently reviewable assignments; the coordinator remains responsible for integration and user communication.
- Keep the shared design contract and evidence rules understandable outside Replit so the workflow can later be adapted to other AI systems.
- Build no user-facing app until repeated real tasks show that an interface would remove meaningful friction.

## 10. Pilot and success criteria

The existing Robot V1 brief and CAD source are a candidate mechanical pilot, not a correctness baseline: parts of that model are preliminary packaging envelopes and require engineering validation.

The pilot succeeds when the workflow can:

- Capture requirements and research scope without losing the user's intent
- Keep dimensions, coordinate systems, and assumptions consistent
- Produce importable STEP geometry and a useful SolidWorks handoff
- Identify limitations and failed checks instead of overstating confidence
- Demonstrate that the independent review and deterministic checks catch issues

After the mechanical pilot, extend the workflow to 2D drawings and PCB drafts. Add other design disciplines only as concrete needs arise.
