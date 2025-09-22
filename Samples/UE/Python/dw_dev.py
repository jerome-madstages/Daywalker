import json, urllib.parse, urllib.request, urllib.error

DEVCHAT_BASE = "http://127.0.0.1:8092"  # No trailing slash

def _post_ask(q: str, timeout: float = 30.0) -> dict:
    url  = f"{DEVCHAT_BASE}/dev/ask"
    data = json.dumps({"q": q}).encode("utf-8")
    req  = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def _get_ask(q: str, timeout: float = 30.0) -> dict:
    qs   = urllib.parse.urlencode({"q": q})
    url  = f"{DEVCHAT_BASE}/dev/ask_get?{qs}"
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

def ask(q: str) -> str:
    q = (q or "").strip()
    if not q:
        return "(error: empty question)"
    try:
        j = _post_ask(q)
        if j.get("ok"): 
            return j.get("answer","").strip()
        # POST returned ok:false -> surface error and try GET as a backup
        err = j.get("error","unknown")
        try:
            j2 = _get_ask(q)
            if j2.get("ok"): 
                return j2.get("answer","").strip()
            return f"(error: {err}; get:{j2.get('error','unknown')})"
        except Exception as e2:
            return f"(error: {err}; get:{e2})"
    except urllib.error.HTTPError as e:
        # HTTP-level failure on POST; try GET
        try:
            j2 = _get_ask(q)
            if j2.get("ok"):
                return j2.get("answer","").strip()
            return f"(error: HTTP {e.code}; get:{j2.get('error','unknown')})"
        except Exception as e2:
            return f"(error: HTTP {e.code}; get:{e2})"
    except Exception as e:
        # Any other failure; try GET
        try:
            j2 = _get_ask(q)
            if j2.get("ok"):
                return j2.get("answer","").strip()
            return f"(error: {e}; get:{j2.get('error','unknown')})"
        except Exception as e2:
            return f"(error: {e}; get:{e2})"
