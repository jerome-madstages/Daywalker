import os, json, argparse, textwrap, urllib.request, pathlib

PORT = int(os.environ.get("DW_RUNNER_PORT", "8081"))
HOST = os.environ.get("DW_RUNNER_HOST", "127.0.0.1")
RUNNER = f"http://{HOST}:{PORT}/v1/chat/completions"
ROOT = os.path.expandvars(r"%USERPROFILE%/Daywalker/LocalTest")
PERSONA_DIR = os.path.join(ROOT, "Personas")

MAX_ITEMS = 8
MAX_MEM_CHARS = 1200

def load_json(path, fallback):
    try:
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    except: return fallback

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def trim_memory(mem):
    mem = mem[-MAX_ITEMS:]; s=""; out=[]
    for item in mem[::-1]:
        cand = (json.dumps(item, ensure_ascii=False)+"\n")+s
        if len(cand) <= MAX_MEM_CHARS: out.append(item); s=cand
        else: break
    return out[::-1]

def build_messages(persona, memory_list, user_prompt):
    sys = f"You are {persona.get('role','an assistant')}. Style: {persona.get('style','concise')}. Safety: {persona.get('safety_note','respond safely')}."
    mem_lines = [f"{m.get('speaker','USER')}: {m.get('text','')}" for m in memory_list]
    mem_block = "\n".join(mem_lines) if mem_lines else "(no prior memory)"
    instr = "Use memory if relevant. Answer briefly and directly. Do not invent lore."
    user = f"Recent memory:\n{mem_block}\n\nCurrent user: {user_prompt}\n{instr}"
    return [{"role":"system","content":sys},{"role":"user","content":user}]

def call_runner(messages):
    body = json.dumps({"model":"local","temperature":0.2,"max_tokens":120,"messages":messages,"stop":["</s>"]}).encode("utf-8")
    req = urllib.request.Request(RUNNER, data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    ch = data.get("choices", [])
    return ch[0]["message"].get("content","").strip() if (ch and "message" in ch[0]) else ""

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", help="persona name (e.g., Guard, Merchant). Defaults to base Persona.json", default=None)
    ap.add_argument("--say", help="store a fact in memory (no model call)", default=None)
    ap.add_argument("--ask", help="ask the model; memory and persona are injected", default=None)
    args = ap.parse_args()

    # Resolve persona file and memory file
    if args.persona:
        persona_path = os.path.join(PERSONA_DIR, f"{args.persona}.json")
        mem_path = os.path.join(ROOT, f"Memory_{args.persona}.json")
    else:
        persona_path = os.path.join(ROOT, "Persona.json")
        mem_path = os.path.join(ROOT, "Memory.json")

    persona = load_json(persona_path, {})
    memory = load_json(mem_path, [])

    changed = False
    if args.say:
        memory.append({"speaker":"USER","text":args.say}); changed = True

    reply = ""
    if args.ask:
        memory = trim_memory(memory)
        messages = build_messages(persona, memory, args.ask)
        reply = call_runner(messages)
        if reply:
            memory.append({"speaker":"ASSISTANT","text":reply}); changed = True

    if changed: save_json(mem_path, memory)
    if reply: print(reply)
