---
name: Design assistant scope
description: The intended scope and software-selection behavior for the engineering design assistant.
---

This project is an engineering design assistant for the user's own work, not a system for copying the appearance of a product from a reference. Autodesk Fusion is the planned primary CAD target, while the system should continue supporting multiple CAD, drafting, electronics, and related tools.

Ask which software the user is using for each design task, and ask for its version or operating system when compatibility or instructions depend on them. Make clear whether the agent can operate that software directly or can only provide compatible files, scripts, or instructions.

**Why:** The user plans to make Autodesk Fusion the primary CAD target while still using other software for some tasks, and wants the assistant to ask which software they are using.

**How to apply:** Include a software-selection question in every design intake. Keep software-specific handoffs and tool-capability checks separate from the core, platform-neutral design brief.
