---
name: pcb-design
description: Plans, drafts, or reviews circuit-board work and its CAD handoff. Use for PCB requirements, schematics, board layouts, KiCad or other EDA projects, and electronics verification.
---

# PCB Design

Follow the engineering-design coordinator Skill. Ask which EDA software and version the user is using; do not assume KiCad. Confirm whether the request is a conceptual schematic, an editable native project, a routed PCB, fabrication outputs, or mechanical-fit geometry.

## Requirements before design

Record the intended function, supply/battery range, current and load estimates, interfaces, connectors, environment, board/enclosure limits, safety/isolation needs, manufacturing constraints, and known component choices. Keep unknown loads and specifications visible.

Do not invent a component pinout, current rating, protection capability, or thermal limit. Use an allowed research scope and cite datasheets/standards for sourced values. Ask before substituting a component or changing a critical electrical interface.

## Native project and tool access

- Prefer an editable project in the user's selected EDA tool. KiCad is one possible target, not an assumed requirement.
- Check whether the application/CLI is available and run a small, non-destructive open/export/check smoke test before substantial board work.
- If the target EDA tool is unavailable, state that limitation; provide files or instructions only when their format can be generated and checked reliably.
- Keep the board's mechanical envelope and connector interfaces coordinated with the mechanical CAD contract.

## Checks and handoff

Run available schematic/ERC, netlist, PCB/DRC, and manufacturing-rule checks. Record warnings as well as errors and do not relabel a blocked check as a pass. Simulation is not measurement; label estimated values, simulated values, and physical test results separately.

Deliver only the formats requested. When requested and supported, these may include the native project, manufacturing outputs such as Gerbers/drill files, a parts list, and a STEP board model for enclosure fit. Do not call the board fabrication-ready until the relevant checks and manufacturer's constraints have been reviewed.

Have a human review schematic readability and board connectors/orientation; zero DRC/ERC errors do not prove that the design meets its intended behavior.

