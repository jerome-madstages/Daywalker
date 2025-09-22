# Dev Chat (Pops-lite)

Purpose
Local developer chat for Unreal + Daywalker. Uses llama.cpp server on 8081 and a small FastAPI proxy on 8092.

Prereqs
- Python 3.10+
- llama-cpp-python server running on 127.0.0.1:8081 with a local model (e.g., Mistral 7B instruct GGUF)
- fastapi + uvicorn installed for the proxy

Start runner (example)
python -m llama_cpp.server --model D:\Models\mistral-7b-instruct-q4_K_M.gguf --host 127.0.0.1 --port 8081 --n_ctx 4096

Start proxy
# Windows
./DevChat/start_devchat_proxy.ps1     # or: uvicorn devchat_proxy:app --host 127.0.0.1 --port 8092 --reload

Health checks
- Runner:  GET http://127.0.0.1:8081/v1/models or POST /v1/completions
- Proxy:   GET http://127.0.0.1:8092/dev/health or open /devchat in a browser

UE integration
Copy Samples/UE/Python/dw_dev.py into YourProject/Content/Python/ then in the UE Python console:
import dw_dev; print(dw_dev.ask("How do I save the current level?"))

Notes
- Ports: runner 8081, proxy 8092
- Scope: Unreal-first; Unity adaptation planned later
- Current behavior: small built-in UE5 knowledge base + strict Unreal-only system prompt
