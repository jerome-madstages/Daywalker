import os, re, json, urllib.request, urllib.parse, random
from flask import Flask, request, jsonify

# --- Config ---
RUNNER_HOST = "127.0.0.1"
RUNNER_PORT = int(os.environ.get("DW_RUNNER_PORT", "8081"))
BASE_DIR    = os.path.join(os.path.expanduser("~"), "Daywalker", "LocalTest")

# --- Persona memory helpers ---
def mem_path(persona:str)->str:
    safe = re.sub(r"[^A-Za-z0-9_-]+","", persona or "Default")
    return os.path.join(BASE_DIR, f"Memory_{safe}.json")

def mem_read(persona:str)->list:
    p = mem_path(persona)
    try:
        with open(p,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def mem_append(persona:str, speaker:str, text:str):
    p = mem_path(persona)
    buf = mem_read(persona)
    buf.append({"speaker": speaker, "text": text})
    try:
        with open(p,"w",encoding="utf-8") as f:
            json.dump(buf, f, ensure_ascii=False, indent=2)
    except:
        pass

# --- Runner call ---
def call_runner(messages, temperature=0.15, top_p=0.6, max_tokens=64, repeat_penalty=1.08, stop=None):
    url = f"http://{RUNNER_HOST}:{RUNNER_PORT}/v1/chat/completions"
    body = {
        "model": "local",
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "repeat_penalty": repeat_penalty,
    }
    if stop:
        body["stop"] = stop
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        out = json.loads(resp.read().decode("utf-8"))
    try:
        return (out["choices"][0]["message"]["content"] or "").strip()
    except:
        return ""

# --- Persona rules injected into prompt ---
def persona_rules(persona:str)->str:
    p = (persona or "").strip().lower()
    if p == "merchant":
        return (
            "ROLE: You are a medieval merchant. "
            "FORMAT: Output exactly ONE line using this pattern:\n"
            "Item — short benefit — N gold.\n"
            "RULES: No lists, no preface, no quotes. Keep it under 80 chars.\n"
            "EXAMPLES:\n"
            "Lockpick set — open simple locks — 7 gold.\n"
            "Grappling hook — climbs — 10 gold.\n"
            "Tinderbox — start fires — 2 gold."
        )
    if p == "guard":
        return (
            "ROLE: You are a gate guard. "
            "If memory mentions a bronze/silver/gold pass, answer: "
            "'The player has a <color> pass.' "
            "FORMAT: one short sentence, nothing else."
        )
    if p == "healer":
        return (
            "ROLE: You are a practical healer. "
            "FORMAT: Output exactly THREE comma-separated items as a kit, like:\n"
            "Carry: Water, Bandages, Torch\n"
            "RULES: No prefaces like 'You should', no numbering, no extra words."
        )
    return (
        "Be concise. One short line if possible. No roleplay. No extra preambles."
    )

# --- Merchant post-processing (force pattern) ---
_MERCH_ITEMS = [
    "Rope", "Lockpick set", "Grappling hook", "Tinderbox", "Torch", "Flint",
    "Oil flask", "Bedroll", "Waterskin", "Compass", "Small knife"
]
_MERCH_BENEFITS = [
    "climbs", "open simple locks", "start fires", "light at night",
    "secure gear", "mark a trail", "camp comfort", "carry water"
]

def normalize_merchant(ans:str)->str:
    s = (ans or "").replace("\n"," ").strip()
    # Try to pull a price
    m = re.search(r"(\d{1,3})\s*gold", s, flags=re.I)
    price = None
    if m:
        try:
            price = int(m.group(1))
        except:
            price = None
    if price is None or price < 1 or price > 50:
        price = random.choice([2,5,7,10])

    # Try to find a known item; fallback random
    item = None
    for it in _MERCH_ITEMS:
        if re.search(rf"\b{re.escape(it.lower())}\b", s.lower()):
            item = it
            break
    if not item:
        item = random.choice(_MERCH_ITEMS)

    # Try to find a succinct benefit; fallback heuristic
    benefit = None
    for b in _MERCH_BENEFITS:
        if re.search(rf"\b{re.escape(b.lower())}\b", s.lower()):
            benefit = b
            break
    if not benefit:
        # Pull a short verb/noun chunk
        c = re.search(r"(climb|lock|fire|light|carry|secure|trail|camp|water)", s.lower())
        benefit = {
            "climb":"climbs","lock":"open simple locks","fire":"start fires",
            "light":"light at night","carry":"carry gear",
            "secure":"secure gear","trail":"mark a trail","camp":"camp comfort",
            "water":"carry water"
        }.get(c.group(1) if c else "", "useful on the road")

    return f"{item} — {benefit} — {price} gold."

# --- Healer post-processing (exactly 3 items) ---
_HEALER_WHITELIST = [
    "Water", "Bandages", "Antiseptic ointment", "Salve",
    "Needle and thread", "Torch", "Flint", "Food rations",
    "Map", "Compass"
]

def normalize_healer(ans:str)->str:
    s = (ans or "").replace("\n"," ")
    s = re.sub(r"(?i)\b(carry|the|and|before|heading|into|forest|you|should|following|items?|list|answer|briefly)\b"," ", s)
    s = re.sub(r"[^A-Za-z0-9 ,'\-]+"," ", s)
    toks = [t.strip() for t in re.split(r"[,\u2022;]|(?:\s+\d+[\).\:]?\s*)", s) if t.strip()]

    # score tokens against whitelist (simple contains)
    picked = []
    for w in _HEALER_WHITELIST:
        for t in toks:
            if w.lower() in t.lower() and w not in picked:
                picked.append(w)
                break

    # top up to 3 with defaults
    defaults = ["Water","Bandages","Torch","Antiseptic ointment","Flint","Needle and thread"]
    for d in defaults:
        if len(picked) >= 3: break
        if d not in picked:
            picked.append(d)

    return "Carry: " + ", ".join(picked[:3])

# --- Guard post-processing (one clean line) ---
def normalize_guard(mem_blob:str, ans:str)->str:
    blob = (mem_blob or "").lower()
    if "bronze pass" in blob:
        return "The player has a bronze pass."
    if "silver pass" in blob:
        return "The player has a silver pass."
    if "gold pass" in blob:
        return "The player has a gold pass."
    # Fallback from model answer
    a = (ans or "").lower()
    if "bronze" in a: return "The player has a bronze pass."
    if "silver" in a: return "The player has a silver pass."
    if "gold"   in a: return "The player has a gold pass."
    return "The player has a pass."

# --- Flask app ---
app = Flask(__name__)

@app.route("/health")
def health():
    try:
        url = f"http://{RUNNER_HOST}:{RUNNER_PORT}/v1/models"
        with urllib.request.urlopen(url, timeout=5) as resp:
            models = json.loads(resp.read().decode("utf-8"))
        return jsonify({"ok": True, "runner_port": RUNNER_PORT, "models": models})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 503

@app.route("/say")
def say():
    persona = (request.args.get("persona","") or "Default").strip()
    text    = (request.args.get("text","")    or "").strip()
    if not text:
        return jsonify({"ok": False, "error": "missing text"}), 400
    mem_append(persona, "USER", text)
    return jsonify({"ok": True, "persona": persona})

@app.route("/ask")
def ask():
    persona = (request.args.get("persona","") or "Default").strip()
    q       = (request.args.get("q","") or "").strip()

    # Compose memory
    memory  = mem_read(persona)[-6:]
    mem_lines = []
    for m in memory:
        sp = m.get("speaker","USER")
        tx = (m.get("text","") or "").strip()
        if tx:
            mem_lines.append(f"{sp}: {tx}")
    mem_blob = "RECENT MEMORY:\n" + "\n".join(mem_lines) if mem_lines else "RECENT MEMORY:\n(none)"

    # Persona instruction
    rules = persona_rules(persona)

    messages = [
        {"role":"system","content": "You are concise. Obey persona rules strictly. Never add extra prefaces or lists."},
        {"role":"user","content": f"{rules}\n\n{mem_blob}\n\nQuestion: {q}\nAnswer now."}
    ]

    # Persona-specific decoding
    temp  = 0.15
    top_p = 0.6
    max_t = 64
    stops = ["\n\n", "RECENT MEMORY", "Question:", "Assistant:", "User:"]

    raw = call_runner(messages, temperature=temp, top_p=top_p, max_tokens=max_t, repeat_penalty=1.08, stop=stops) if q else ""

    # Post-process
    if persona.lower() == "merchant":
        answer = normalize_merchant(raw)
    elif persona.lower() == "healer":
        answer = normalize_healer(raw)
    elif persona.lower() == "guard":
        answer = normalize_guard(mem_blob, raw)
    else:
        answer = (raw or "").splitlines()[0].strip() if raw else ""

    if answer:
        mem_append(persona, "ASSISTANT", answer)

    return jsonify({"ok": True, "persona": persona, "answer": answer})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090)
