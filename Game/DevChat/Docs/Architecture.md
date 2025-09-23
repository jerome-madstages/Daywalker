# Architecture

Scope
Unreal-first developer chat (Dev Chat, “Pops-lite”) that runs locally: UE Python helper → FastAPI proxy → llama.cpp runner. No cloud dependency.

Components
- Unreal Editor: uses Python helper `dw_dev.py` for Q/A.
- Dev Chat proxy: FastAPI app on 127.0.0.1:8092; routes /dev/ask and exposes /devchat page.
- Runner: llama_cpp.server on 127.0.0.1:8081, serving /v1/completions and /v1/chat/completions.
- Model: local GGUF file loaded by the runner (“model”: "local").

Signal flow
UE Python (dw_dev.ask)
    -> HTTP POST 127.0.0.1:8092/dev/ask  (JSON {"q": "..."})
    -> Proxy composes strict Unreal/Daywalker prompt; small UE5 KB answers some questions directly
    -> Proxy -> Runner POST 127.0.0.1:8081/v1/completions (fallback to /v1/chat/completions)
    -> Runner returns text
    -> Proxy returns {"ok": true, "answer": "..."}
    -> UE prints answer in the Python console

ASCII diagram
[ UE Editor ]
   |  dw_dev.py (ask)
   v
[ Dev Chat Proxy :8092 ] --fallback--> [ /v1/chat/completions ]
   |  /dev/ask                            ^
   v                                      |
[ Runner :8081 ] <- /v1/completions ------+
   (llama_cpp.server, model="local")

Ports and env
- Runner: 8081
- Proxy: 8092
- Override runner URL for proxy: set RUNNER_URL=http://127.0.0.1:8081
- Model name in requests: "local"

Files and locations
- DevChat/devchat_proxy.py            (FastAPI proxy)
- Samples/UE/Python/dw_dev.py         (UE helper)
- Scripts/diagnose_daywalker.ps1      (quick health/Q/A check)
- Media/                              (screenshots)
- Docs/Quickstart.md, Docs/Troubleshooting.md, Docs/DevChat.md, Docs/Architecture.md, Docs/Glossary.md

Health checks
- Runner: POST /v1/completions {"model":"local","prompt":"ping","max_tokens":1}
- Proxy:  GET  /dev/health ({"ok": true}), open /devchat in a browser

Behavioral guardrails
- Unreal/Daywalker-only answers via system prompt; if Unity is mentioned, proxy returns a constrained reply.
- Tiny built-in UE5 KB provides deterministic answers for common tasks (save level, screenshots path, etc.).

Planned extensions (tracked in Docs/ROADMAP.md)
- Editor Utility Widget UI (no PySide2 dependency).
- External KB loader for proxy.
- Multiple personas for Dev Chat (Dev, Designer, QA).
- Project-aware context, streaming, memory persistence.
