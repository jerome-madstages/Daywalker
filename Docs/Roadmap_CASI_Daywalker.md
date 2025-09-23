CASI: Daywalker Roadmap

Context
Day 7 establishes the baseline: local runner on 8081, Dev Chat proxy on 8092, UE Python helper, working Q→A, docs and media.

v0.2 (short term)
Goals
• In-editor access without PySide2 dependency
• Externalize and grow the UE5 knowledge base
• Small UX and robustness upgrades
Work
• Editor Utility Widget with a text box and Ask button that calls dw_dev.ask
• Proxy loads kb_ue.txt from DevChat/ at startup; hot-reload on file change
• Streaming replies path in proxy (optional if model supports it)
• Scripts: start and stop stack refined; diagnostics prints model and ports

v0.3 (near term)
Goals
• Project-aware context and basic memory
Work
• Summarize Content/ and Config/ into lightweight context notes the proxy can read
• Add optional per-project chat log (JSONL or SQLite) with explicit on/off
• Expand Docs/Troubleshooting and provide more guided examples

v0.4 (mid term)
Goals
• Personas and early Unity adapter
Work
• Persona routing in proxy (?persona=Dev|Designer|QA) and per-persona prompts
• Unity adapter plan and skeleton; keep Unreal as primary
• Additional samples and a tighter demo map

Phase 2: Avatars
Focus
• NPC avatars and interaction scaffolds
• Authoring flow for Persona and Memory artifacts
Deliverables
• Example NPCs with clear prompt stacks and behaviors
• Demo scenes and repeatable test cases

Phase 3: Stadium VR integration
Focus
• Scaled multi-actor interactions in a performance-constrained scene
Deliverables
• Integration plan and prototype scene
• Performance instrumentation and documentation

Phase 4: MAGI System
Focus
• Converge toward CASI’s symbolic intelligence path
• Pops-lite evolution toward conversational Pops
Deliverables
• Bridging model between the current pipeline and CASI symbolic runtime
• Migration notes and constraints

GuestAI and ResidentAI (positioning)
• GuestAI: transient, task-scoped assistants layered on Dev Chat
• ResidentAI: project-scoped, memory-bearing assistants with explicit controls
• First appearance targeted for the v0.3–v0.4 window in limited form

Reviewer guidance
• Today: a working, offline Unreal developer chat with clean docs and media
• Next releases expand scope methodically without adding cloud dependencies
