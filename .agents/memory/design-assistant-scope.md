---
name: Design assistant scope
description: The intended scope and software-selection behavior for the engineering design assistant.
---

This project is an engineering design assistant for the user's own work, not a system for copying the appearance of a product from a reference. It should support multiple CAD, drafting, electronics, and related tools rather than assuming SolidWorks.

Ask which software the user is using for each design task, and ask for its version or operating system when compatibility or instructions depend on them. Make clear whether the agent can operate that software directly or can only provide compatible files, scripts, or instructions.

**Why:** The user intends to use the system for CAD design across SolidWorks, AutoCAD, and other software, and wants the assistant to ask which software they are using.

**How to apply:** Include a software-selection question in every design intake. Keep software-specific handoffs and tool-capability checks separate from the core, platform-neutral design brief.
