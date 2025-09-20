# UE Dashboard Sketch (Editor Utility Widget)

Purpose
- One in-editor panel to ping health, pick persona, ask/say, and capture.

Elements
- Status: shows runner port and model id, and proxy health OK/FAIL
- Persona: dropdown [Merchant, Guard, Healer]
- Ask input: single-line text; Ask button posts to /ask
- Say input: single-line text; Say button posts to /say
- Capture: buttons [Screenshot x3], [Record 20s]
- Memory: buttons [Open persona JSON], [Clear memory]

Implementation notes
- Create an Editor Utility Widget (BP) named DW_Dashboard
- Buttons call simple Python hooks (dw_query.ask/say) or Blueprint HTTP
- Store widget asset under Content/Editor/DW_Dashboard.uasset
- Acceptance: all actions work without leaving the panel
