# Demo Recipe

Goal
- Produce 3 screenshots (Merchant, Guard, Healer) and a 15–30s clip showing on-screen updates.

Prereqs
- Runner on 8081 and Proxy on 8090 are running and healthy.
- UE Editor is open to the DaywalkerDemo project level.

Steps
1) Place text and capture screenshots (UE Python Console)
import os, time, unreal, dw_query
OUT = os.path.join(os.path.expanduser("~"), "Documents", "Daywalker_Captures"); os.makedirs(OUT, exist_ok=True)
def shot(label, persona, q):
    s = dw_query.ask(persona, q) or "(no answer)"
    unreal.SystemLibrary.print_string(None, f"{label}: {s}", True, True, 4.0)
    time.sleep(0.4)
    unreal.AutomationLibrary.take_high_res_screenshot(1920,1080, os.path.join(OUT, f"{label}.png"))
shot("Merchant","Merchant","Offer me something new.")
shot("Guard","Guard","What pass does the player have?")
shot("Healer","Healer","What should I carry before heading into the forest?")

2) Record a short clip (screen recorder)
- Start recording, then in UE Python Console:
import time, unreal, dw_query
unreal.SystemLibrary.print_string(None, "Recording…", True, True, 3.0); time.sleep(3.0)
unreal.SystemLibrary.print_string(None, "Merchant: "+(dw_query.ask("Merchant","Offer me something new.") or ""), True, True, 5.0); time.sleep(5.0)
unreal.SystemLibrary.print_string(None, "Guard: "+(dw_query.ask("Guard","What pass does the player have?") or ""), True, True, 5.0); time.sleep(5.0)
unreal.SystemLibrary.print_string(None, "Healer: "+(dw_query.ask("Healer","What should I carry before heading into the forest?") or ""), True, True, 5.0); time.sleep(3.0)
unreal.SystemLibrary.print_string(None, "Demo complete.", True, True, 2.0)

3) Trim if needed and store in
%USERPROFILE%\Documents\Daywalker_Captures\Clips

Tips
- If text appears too small, move the editor camera closer before running.
- If text overlaps, run the prints one at a time with short delays.
