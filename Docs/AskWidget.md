# Ask Daywalker (Editor Utility Widget)

Summary
A small Editor Utility Widget that sends your question to the local Dev Chat proxy and shows the reply.

Prereqs
• Dev Chat proxy on 8092; runner on 8081.  
• Project has Python helpers: Samples/UE/Python/dw_toast.py and register_daywalker_menu.py.  
• Plugins enabled: Python Editor Script Plugin, Editor Scripting Utilities.

Designer
1) Add Vertical Box.
2) Add Text (label): set Text = "Ask Daywalker" (optional center, size ~18).
3) Add Editable Text Box: check Is Variable (header), Name = QBox, set Hint Text.
4) Add Button: inside it add Text "Ask". Name the Button = AskButton. Save.

Graph
1) Select AskButton → Details → Events → + On Clicked.
2) Drag QBox into graph (Get) → Get Text → ToString.
3) Optional: Set Q (String) = ToString.
4) Escape and build command:
   • Replace "\" → "\\" then Replace "'" → "\'".
   • Append: A + [escaped] + B, where
     A = `import importlib, dw_dev, dw_toast; importlib.reload(dw_dev); importlib.reload(dw_toast); q='`
     B = `'; dw_toast.ask_and_toast(q)`
   • Set Cmd (String) = result.
5) Execute Python Command (Command = Cmd).
6) After exec: Set Text(QBox,"") then Set Keyboard Focus(QBox).
7) Compile, Save. Run via Window → Editor Utilities → Utility Widget.

Notes
If `dw_dev` not found, set once in Python console:
  import importlib, dw_dev
  dw_dev.DEVCHAT_BASE="http://127.0.0.1:8092"
  importlib.reload(dw_dev)
