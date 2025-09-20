# Quickstart

1) Start services
- Double-click Start-Daywalker-Runner (wait for “Uvicorn running on http://127.0.0.1:8081”)
- Double-click Start-Daywalker-Demo (wait for “Running on http://127.0.0.1:8090”)

2) Health checks (PowerShell)
Invoke-WebRequest "http://127.0.0.1:8081/v1/models" | Select-Object -ExpandProperty Content
Invoke-WebRequest "http://127.0.0.1:8090/health"     | Select-Object -ExpandProperty Content

3) Open the UE project if it didn’t auto-open
& "D:\Unreal Engine\UE_5.5\UnrealEngine\Engine\Binaries\Win64\UnrealEditor.exe" `
  "$env:USERPROFILE\Documents\Unreal Projects\DaywalkerDemo\DaywalkerDemo.uproject"

4) Sanity prompt (UE Python Console)
import dw_query
print(dw_query.ask("Merchant","Offer me something new."))

5) One screenshot (UE Python Console)
import os, time, unreal, dw_query
out_dir = os.path.join(os.path.expanduser("~"), "Documents", "Daywalker_Captures")
os.makedirs(out_dir, exist_ok=True)
ans = dw_query.ask("Guard","What pass does the player have?") or "(no answer)"
unreal.SystemLibrary.print_string(None, "Guard: "+ans, True, True, 6.0)
time.sleep(0.5)
unreal.AutomationLibrary.take_high_res_screenshot(1920,1080, os.path.join(out_dir,"guard_check.png"))

6) Find your assets
Screenshots: %USERPROFILE%\Documents\Daywalker_Captures
Clips:      %USERPROFILE%\Documents\Daywalker_Captures\Clips
