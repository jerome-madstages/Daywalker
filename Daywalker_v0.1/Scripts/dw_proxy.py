from flask import Flask, request, jsonify
import os, json, urllib.request

HOST = "127.0.0.1"
RUNNER_PORT = int(os.environ.get("DW_RUNNER_PORT","8081"))
RUNNER = f"http://{HOST}:{RUNNER_PORT}/v1/chat/completions"

ROOT = os.path.expandvars(r"%USERPROFILE%/Daywalker/LocalTest")
PERSONA_DIR = os.path.join(ROOT, "Personas")

def load_persona(name):
    path = os.path.join(PERSONA_DIR, f"{name}.json")
    if not os.path.exists(path):
        return {"role":"an NPC","style":"concise","safety_note":"respond safely"}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def call_runner(messages):
    body = json.dumps({
        "model":"local","temperature":0.2,"max_tokens":120,
        "messages":messages,"stop":["</s>"]
    }).encode("utf-8")
    req = urllib.request.Request(RUNNER, data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ch = data.get("choices", [])
    return ch[0]["message"].get("content","").strip() if (ch and "message" in ch[0]) else ""

app = Flask(__name__)

@app.get("/ask")
def ask():
    persona = request.args.get("persona","Guard")
    q = request.args.get("q","")
    p = load_persona(persona)
    sys_msg = {
        "role":"system",
        "content": f"You are {p.get('role')}. Style: {p.get('style')}. Safety: {p.get('safety_note')}."
    }
    user_msg = {"role":"user","content": f"{q}\nAnswer briefly. Do not roleplay both sides."}
    answer = call_runner([sys_msg, user_msg]) if q else ""
    return jsonify({"persona": persona, "answer": answer})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090)
