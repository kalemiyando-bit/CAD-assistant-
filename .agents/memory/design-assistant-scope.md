---
name: Design assistant scope
description: The intended scope and software-selection behavior for the engineering design assistant.
---

This project is a system for helping the user build CAD designs through Replit Agent and other Replit agents. It is not a web app or a standalone Python app, and it is not a system for copying the appearance of a product from a reference. Autodesk Fusion is the planned primary CAD target, while the system should continue supporting multiple CAD, drafting, electronics, and related tools.

The system is a conversational, Replit-first workflow that uses Replit's Agent environment and project Skills to help the user with engineering and CAD design. It is not intended to be a conventional web app or a standalone Python application. Python scripts may serve as bridges or helpers for CAD software, but they are not the product.

Ask which software the user is using for each design task, and ask for its version or operating system when compatibility or instructions depend on them. Make clear whether the agent can operate that software directly or can only provide compatible files, scripts, or instructions.

For early system testing, the user wants to describe a design conversationally, receive a clearly labeled preliminary draft, and continue developing it in Fusion. The user usually turns 2D drawings into 3D models, but the purpose can vary by job. Test one simple part at a time: start with its 2D drawing, then its 3D model, before expanding to other parts, assemblies, safety/control design, and PCB work. Before making a 2D deliverable, ask whether it is for building 3D geometry, documentation, or both; use separate outputs, and keep borders and annotation geometry out of model-building sketches. Do not block these tests on manufacturing-release completeness; keep assumptions and unverified limits explicit. Document exact Skills, scripts, and checks so other agents can reuse methods already tested.

**Why:** The user emphasized that CAD Assistant exists to help them and other Replit agents build CAD designs; a conventional web app or standalone Python app is not the product. They also asked that agents reuse documented methods and not rediscover the implementation path. The user's successful Fusion DXF import showed that sheet frames and dimension graphics become sketch entities, so the intended use must be settled before choosing the 2D output. Autodesk Fusion is the user's primary CAD target, with support for other tools.

**How to apply:** Include a software-selection question in every design intake. For 2D work, ask the modeling-versus-documentation question before generation and create separate outputs when both are needed. Keep software-specific handoffs and tool-capability checks separate from the core, platform-neutral design brief. In early system tests, follow the user's staged 2D-then-3D sequence and wait for Fusion feedback before broadening scope.
