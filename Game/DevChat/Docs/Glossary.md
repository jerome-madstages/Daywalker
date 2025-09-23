# Glossary

Daywalker
Prototype UE toolchain that integrates local LLM capabilities into editor workflows.

Dev Chat (Pops-lite)
Local developer chat for Unreal/Daywalker. UE Python helper calls a proxy which calls a local model runner.

Runner
llama_cpp.server process exposing /v1/completions and /v1/chat/completions on 127.0.0.1:8081.

Proxy
FastAPI service on 127.0.0.1:8092. Endpoints:
- /dev/ask (POST) – primary JSON API
- /dev/ask_get (GET) – fallback for simple clients
- /dev/health (GET) – health probe
- /devchat (GET) – simple HTML page for local testing

dw_dev.py
UE Python helper located at Samples/UE/Python/dw_dev.py. Provides ask(q) → str using /dev/ask.

Diagnose script
Scripts/diagnose_daywalker.ps1. Verifies runner, proxy, and a sample Q/A.

Default maps
EditorStartupMap and GameDefaultMap set to /Game/Daywalker_DevChat in Config/DefaultEngine.ini.

Media
Screenshots stored in Media/ (repo) and in Project/Saved/Screenshots/Windows (UE output).

Persona.json, Memory.json
Scaffolds for NPC-facing features (not used by Dev Chat yet).

PromptComposer
Template logic for NPC prompts (placeholder if not yet committed in this repo).

Ports
8081 (runner), 8092 (proxy).

Knowledge base (UE5 KB)
Small set of canned answers in the proxy for common Unreal tasks; used before model calls.
