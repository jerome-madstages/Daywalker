param(
  [string]$UEEditor = "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe",
  [string]$UProject = "$env:USERPROFILE\Documents\Unreal Projects\DaywalkerDemo\DaywalkerDemo.uproject",
  [string]$Model    = "D:\Models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Start-Process powershell -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-File', (Join-Path $Here 'run_runner.ps1'), '-Model', $Model)
Start-Process powershell -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-File', (Join-Path $Here 'run_proxy.ps1'))
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:8092/devchat"
Start-Process -FilePath $UEEditor -ArgumentList "`"$UProject`""
