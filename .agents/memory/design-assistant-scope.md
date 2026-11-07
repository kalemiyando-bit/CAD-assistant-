---
name: Design assistant scope
description: The intended scope and software-selection behavior for the engineering design assistant.
---

This project is an engineering design assistant for the user's own work, not a system for copying the appearance of a product from a reference. Autodesk Fusion is the planned primary CAD target, while the system should continue supporting multiple CAD, drafting, electronics, and related tools.

The system is a conversational, Replit-first workflow that uses Replit's Agent environment and project Skills to help the user with engineering and CAD design. It is not intended to be a conventional web app or a standalone Python application. Python scripts may serve as bridges or helpers for CAD software, but they are not the product.

Ask which software the user is using for each design task, and ask for its version or operating system when compatibility or instructions depend on them. Make clear whether the agent can operate that software directly or can only provide compatible files, scripts, or instructions.

**Why:** The user clarified that CAD Assistant should use Replit's environment and Agent resources as an engineering workflow, not be built as a conventional web or Python app. Autodesk Fusion is planned as the primary CAD target, with support for other tools.

**How to apply:** Include a software-selection question in every design intake. Keep software-specific handoffs and tool-capability checks separate from the core, platform-neutral design brief.
