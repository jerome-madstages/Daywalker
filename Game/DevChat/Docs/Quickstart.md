# Quickstart (Windows 11, Unreal 5.5.x)

Prereqs
- Python 3.10+
- A local GGUF model file (example path below)
- Git and Unreal Editor 5.5.x
- llama_cpp.server (installed with llama-cpp-python)
- fastapi and uvicorn (proxy)

1) Start the local runner on port 8081
python -m llama_cpp.server --model "D:\Models\mistral-7b-instruct-q4_K_M.gguf" --host 127.0.0.1 --port 8081 --n_ctx 4096

2) Start the Dev Chat proxy on port 8092
Option A: Desktop shortcut Start-Daywalker-DevChat-Proxy.bat
Option B:
cd %USERPROFILE%\Desktop\Daywalker\DevChat
set RUNNER_URL=http://127.0.0.1:8081
python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port 8092 --reload

3) Health checks
# Runner check (expects JSON)
powershell -c "Invoke-RestMethod -Uri http://127.0.0.1:8081/v1/completions -Method POST -ContentType 'application/json' -Body '{""model"":""local"",""prompt"":""ping"",""max_tokens"":1}'"
# Proxy check (expects {"ok": true})
powershell -c "Invoke-RestMethod -Uri http://127.0.0.1:8092/dev/health -Method GET"

4) Unreal Editor test
Copy Samples/UE/Python/dw_dev.py into YourProject/Content/Python/
In the Unreal Python console:
import dw_dev
print(dw_dev.ask("How do I save the current level and where are screenshots stored?"))

5) Optional browser Dev Chat
Open http://127.0.0.1:8092/devchat

Ports and config
- Runner: 8081
- Proxy: 8092
- Override runner URL for the proxy: set RUNNER_URL=http://127.0.0.1:8081
- Model name used by the runner: "local"
