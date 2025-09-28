# Dev Chat (Pops-lite)

Local Unreal developer chat backed by llama.cpp (8081) with a FastAPI proxy (8092).

Quickstart
1. Start runner (8081): `python -m llama_cpp.server --model <your.gguf> --host 127.0.0.1 --port 8081`
2. Start proxy (8092): `python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port 8092 --reload`
3. UE link: set `dw_dev.DEVCHAT_BASE = "http://127.0.0.1:8092"` then `dw_dev.ask("…")`
4. KB files: `kb_ue.jsonl`, `kb_casi.jsonl` (JSONL, one object per line). Reload: `POST /dev/reload_kb`.

In-Editor access
• Menu entry (Window/Help/File): “Daywalker: Open Dev Chat (browser)” and “Daywalker: Ask (from clipboard)”.  
• Editor Utility Widget sample: `AskDaywalker_EUW.uasset` (if present).  
• Helpers: `Samples/UE/Python/dw_toast.py`, `register_daywalker_menu.py`.

Endpoints
• GET /dev/health → `{ok, runner}`  
• POST /dev/ask `{q}` → `{ok, answer, provenance}`  
• POST /dev/reload_kb → `{ok, count}`
