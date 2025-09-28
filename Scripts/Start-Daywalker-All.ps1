# EDIT THESE THREE PATHS FOR YOUR MACHINE BEFORE RUNNING LOCALLY
$UEEditor = "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe"
$UProject = "$env:USERPROFILE\Documents\Unreal Projects\DaywalkerDemo\DaywalkerDemo.uproject"
$Model    = "D:\Models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Derived paths
$RunnerVenv = "$env:USERPROFILE\daywalker-venv\Scripts\Activate.ps1"
$ProxyDir   = "$env:USERPROFILE\Desktop\Daywalker\DevChat"

# Runner (8081)
Start-Process powershell -ArgumentList @(
  '-NoExit','-ExecutionPolicy','Bypass','-Command',
  "& `"$RunnerVenv`"; `"`$Model = `"$Model`"; python -m llama_cpp.server --model `"`$Model`" --host 127.0.0.1 --port 8081 --n_ctx 2048"
)

# Proxy (8092)
Start-Process powershell -ArgumentList @(
  '-NoExit','-ExecutionPolicy','Bypass','-Command',
  "Set-Location `"$ProxyDir`"; `$env:RUNNER_URL = 'http://127.0.0.1:8081'; python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port 8092 --reload"
)

# Open Dev Chat and launch UE
Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:8092/devchat"
Start-Process -FilePath "$UEEditor" -ArgumentList "`"$UProject`""
