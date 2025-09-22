import os, re, json, traceback, httpx
from fastapi import FastAPI, Body, Query
from fastapi.responses import HTMLResponse, JSONResponse

RUNNER_URL = os.environ.get("RUNNER_URL", "http://127.0.0.1:8081")
MODEL      = os.environ.get("MODEL", "local")

app = FastAPI(title="Daywalker Dev Chat Proxy")

SYSTEM_PROMPT = (
    "You are Dev, an assistant for Unreal Engine 5 and the Daywalker UE plugin. "
    "Answer ONLY with Unreal/UE5 and Daywalker-specific steps. "
    "If a question refers to Unity or another engine, reply: "
    "\"This chat is for Unreal/Daywalker; I don't have Unity details.\" "
    "If you are not sure, reply: \"I don't know yet.\" "
    "Be concise and concrete. Prefer standard UE paths and menus."
)

def kb_answer(q: str) -> str | None:
    t = q.lower().strip()

    # save current level
    if ("save" in t and "level" in t) and ("how" in t or "where" in t or "current" in t):
        return (
            "Unreal Editor: File > Save Current Level or press Ctrl+S. "
            "To save all: File > Save All or Ctrl+Shift+S."
        )

    # screenshots location
    if "screenshot" in t or "screen shot" in t:
        return (
            "Editor screenshots are written under Project/Saved/Screenshots/<Platform>/ "
            "(for Windows builds: Saved/Screenshots/Windows). "
            "High-res shots use the HighResShot command and write to the same folder."
        )

    # add/create new level
    if ("add" in t or "create" in t) and "level" in t:
        return (
            "Create a level via File > New Level, or in Content Browser: Add/Import > Level. "
            "Open by double-clicking the .umap. Set default maps in Project Settings > Maps & Modes."
        )

    # import/apply textures
    if ("texture" in t or "material" in t) and ("add" in t or "import" in t or "apply" in t):
        return (
            "Import textures in the Content Browser (Add/Import or drag-and-drop). "
            "Create a Material, assign the Texture Sample nodes, then apply the material to meshes in the Details panel."
        )

    # unity mention guard
    if "unity" in t:
        return "This chat is for Unreal/Daywalker; I don't have Unity details."

    return None

_HTML = """<!doctype html><meta charset="utf-8"><title>Daywalker Dev Chat</title>
<style>body{font:14px system-ui;margin:24px} .log{white-space:pre-wrap;border:1px solid #ddd;padding:10px;border-radius:8px;max-width:900px}</style>
<h2>Daywalker Dev Chat (local)</h2><div id=health>checking…</div><div class=log id=log></div><br>
<input id=q size=80 placeholder="Ask about setup, logs, scripts…"><button onclick="ask()">Ask</button>
<script>
(async()=>{try{const r=await fetch("/dev/health");const j=await r.json();document.getElementById("health").textContent=j.ok?"Runner OK":"Runner offline";}catch{document.getElementById("health").textContent="Health check failed";}})();
async function ask(){const i=document.getElementById("q");const q=i.value.trim(); if(!q)return;
 const L=document.getElementById("log"); L.innerHTML+=`\\n\\nYou: ${q}`;
 const r=await fetch("/dev/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({q})});
 const j=await r.json(); L.innerHTML+=`\\nDaywalker: ${j.ok?j.answer:"(error) " + (j.error||"")}`;}
</script>"""

@app.get("/devchat", response_class=HTMLResponse)
def devchat_page():
    return _HTML

@app.get("/dev/health")
def health():
    try:
        r = httpx.post(f"{RUNNER_URL}/v1/completions",
                       json={"model": MODEL, "prompt": "ping", "max_tokens": 1},
                       timeout=5.0)
        r.raise_for_status()
        return {"ok": True}
    except Exception:
        return {"ok": False}

def _runner_complete(prompt: str, max_tokens: int = 256) -> str:
    # Try /v1/completions
    try:
        r = httpx.post(f"{RUNNER_URL}/v1/completions",
                       json={"model": MODEL, "prompt": prompt, "max_tokens": max_tokens},
                       timeout=30.0)
        r.raise_for_status()
        j = r.json()
        t = (j.get("choices") or [{}])[0].get("text","").strip()
        if t:
            return t
    except Exception:
        pass
    # Fallback: /v1/chat/completions
    r = httpx.post(f"{RUNNER_URL}/v1/chat/completions",
                   json={"model": MODEL,
                         "messages":[{"role":"system","content": SYSTEM_PROMPT},
                                     {"role":"user","content": prompt}]},
                   timeout=30.0)
    r.raise_for_status()
    j = r.json()
    msg = (j.get("choices") or [{}])[0].get("message",{})
    t = msg.get("content","").strip()
    if not t:
        raise RuntimeError("Empty response from /v1/chat/completions")
    return t

def _answer(q: str) -> str:
    # 1) UE5 KB first
    kb = kb_answer(q)
    if kb:
        return kb
    # 2) Prompt with strict system instructions
    prompt = f"{SYSTEM_PROMPT}\nQ: {q}\nA:"
    return _runner_complete(prompt, max_tokens=256)

@app.post("/dev/ask")
def dev_ask(payload: dict = Body(...)):
    try:
        q = (payload or {}).get("q","").strip()
        if not q:
            return JSONResponse({"ok": False, "error": "empty question"})
        return {"ok": True, "answer": _answer(q)}
    except Exception as e:
        err = "".join(traceback.format_exception_only(type(e), e)).strip()
        return JSONResponse({"ok": False, "error": err})

@app.get("/dev/ask_get")
def dev_ask_get(q: str = Query(..., min_length=1)):
    try:
        return {"ok": True, "answer": _answer(q)}
    except Exception as e:
        err = "".join(traceback.format_exception_only(type(e), e)).strip()
        return JSONResponse({"ok": False, "error": err})
