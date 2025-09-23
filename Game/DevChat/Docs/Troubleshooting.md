# Troubleshooting

Runner healthy but proxy returns HTTP 500
- Verify the runner with:
  powershell -c "Invoke-RestMethod -Uri http://127.0.0.1:8081/v1/completions -Method POST -ContentType 'application/json' -Body '{""model"":""local"",""prompt"":""ping"",""max_tokens"":1}'"
- Check the proxy window; errors are printed there. The proxy returns ok:false with an error when possible.

404 Not Found on /devchat
- /devchat is the HTML page; API calls should use:
  POST /dev/ask  or  GET /dev/ask_get?q=...

UE Python console error: unterminated string literal
- Ensure the URL string is on one line and has closing quotes.

UE Python: no PySide2
- The optional panel requires Python Editor Script Plugin and Editor Scripting Utilities plugins enabled and a restart.
- Dev Chat works without PySide2 using the Python console and Samples/UE/Python/dw_dev.py.

Port already in use
- Change the port or close the existing process.
  Proxy: python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port 8093 --reload
  Then set DEVCHAT_BASE in dw_dev.py accordingly.

Default maps not loading on launch
- Defaults are in Config/DefaultEngine.ini under [/Script/EngineSettings.GameMapsSettings].
- EditorStartupMap and GameDefaultMap should both be /Game/Daywalker_DevChat.

Redirectors after asset moves/renames
- In Content Drawer: enable “Sources Panel”, right-click Content (the /Game root) → Fix Up Redirectors in Folder.
- If the menu isn’t present, there are no redirectors to fix.

Deleting a level
- You cannot delete the level that is currently loaded. Load a different map first, then delete.

One-command diagnosis
- Scripts/diagnose_daywalker.ps1 checks runner, proxy, and a sample Q/A.
