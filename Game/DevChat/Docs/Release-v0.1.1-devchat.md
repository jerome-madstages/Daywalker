# Release v0.1.1-devchat

Summary
Prototype Dev Chat (Pops-lite) for Unreal. Local-only path: UE Python helper → FastAPI proxy (8092) → llama.cpp runner (8081). No cloud dependency.

Highlights
- Working round-trip from Unreal Python console via Samples/UE/Python/dw_dev.py
- FastAPI proxy with Unreal-only guardrails and a small UE5 knowledge base
- Diagnose script for quick verification
- Docs: Quickstart, Troubleshooting, Architecture, Glossary
- Screenshot in README

Install and run
1) Start runner
python -m llama_cpp.server --model "D:\Models\mistral-7b-instruct-q4_K_M.gguf" --host 127.0.0.1 --port 8081 --n_ctx 4096

2) Start proxy
DevChat\start_devchat_proxy.ps1

3) Verify
Scripts\diagnose_daywalker.ps1

4) Unreal test
Copy Samples\UE\Python\dw_dev.py to YourProject\Content\Python\
In UE Python console:
import dw_dev
print(dw_dev.ask("How do I save the current level and where are screenshots stored?"))

What works today
- UE → Proxy → Runner Q/A
- Strict Unreal scope; small UE5 KB answers common tasks
- Default maps set to /Game/Daywalker_DevChat

Known limitations
- Minimal UI; PySide2 panel optional and version dependent
- No code awareness or long-term memory yet
- Single model name "local"; adjust runner if needed

Links
- Docs/Quickstart.md
- Docs/Troubleshooting.md
- Docs/Architecture.md
- Docs/Glossary.md
