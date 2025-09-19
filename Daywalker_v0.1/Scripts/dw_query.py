import json, urllib.request, urllib.parse
PROXY = "http://127.0.0.1:8090"
def ask(persona, q):
    u = f"{PROXY}/ask?persona="+urllib.parse.quote(persona)+"&q="+urllib.parse.quote(q)
    with urllib.request.urlopen(u, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8")).get("answer","")
def say(persona, text):
    u = f"{PROXY}/say?persona="+urllib.parse.quote(persona)+"&text="+urllib.parse.quote(text)
    with urllib.request.urlopen(u, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8")).get("ok", False)
