# Daywalker Glossary

Runner
- Local HTTP server powered by llama_cpp.server
- Default: http://127.0.0.1:8081
- Model path in Start-Daywalker-Runner: D:\Models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

Proxy
- Lightweight Flask app at http://127.0.0.1:8090
- Endpoints: /ask?persona=...&q=..., /say?persona=...&text=..., /health
- Composes a system prompt + persona + short memory before calling the Runner

Personas and memory
- Persona memory files (JSON) live here:
  %USERPROFILE%\Daywalker\LocalTest\Memory_Guard.json
  %USERPROFILE%\Daywalker\LocalTest\Memory_Merchant.json
  %USERPROFILE%\Daywalker\LocalTest\Memory_Healer.json
- Used for tiny recall (e.g., guard pass, merchant price, healer advice)

UE integration (Editor)
- Python Console: Window → Developer Tools → Python Console
- Output Log: Window → Developer Tools → Output Log
- No gameplay C++ required for the demo; we drive it via Editor Python

Capture locations
- Screenshots (automatic): %USERPROFILE%\Documents\Daywalker_Captures
- UE high-res fallback: %USERPROFILE%\Documents\Unreal Projects\DaywalkerDemo\Saved\Screenshots\Windows
- Clips (manual screen recorder): %USERPROFILE%\Documents\Daywalker_Captures\Clips

Ports
- Runner 8081, Proxy 8090
- Health: Invoke-WebRequest http://127.0.0.1:8081/v1/models ; http://127.0.0.1:8090/health

Desktop shortcuts
- Start-Daywalker-Runner: launches model + runner on 8081
- Start-Daywalker-Demo: launches proxy on 8090, opens UE project

Model choice
- Current: TinyLlama gguf for speed and zero-setup GPU requirements
- Future: Mistral/Llama variants via config toggle in the proxy
