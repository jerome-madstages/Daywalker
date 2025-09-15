README

Daywalker (v1) — UE5 local NPC prototype plug-in

What this is
Daywalker is an open-source Unreal Engine 5 developer plug-in that prototypes conversational NPCs locally and offline. v1 exposes a single Blueprint-callable node that calls a small local model runner. A persona JSON and a fixed PromptComposer template shape behavior. A simple JSON memory stores the last N lines for basic recall.

Scope for v1
• UE5 plug-in shell (C++ with one Blueprint node: QueryLLM)
• Local runner (llama-cpp-python server; buffered output)
• Persona.json + fixed PromptComposer template
• Memory.json last-N log
• Small demo map with two NPCs

Models
We do not ship weights in the repo.
Tested model: Mistral 7B Instruct, GGUF, q4_0
Example local file name: mistral-7b-instruct-v0.1.Q4_0.gguf
Local placement (not committed): ./models/mistral-7b-instruct-v0.1.Q4_0.gguf

Local runner (first test)
Prerequisites: Python 3.10+

Create a virtual environment
python -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate

Install the server
pip install "llama-cpp-python[server]"

Start the server (adjust the model path if different)
python -m llama_cpp.server
--model ./models/mistral-7b-instruct-v0.1.Q4_0.gguf
--host 127.0.0.1
--port 8080
--n_ctx 4096

Health check
curl -s http://127.0.0.1:8080/health

Test a completion
curl -s http://127.0.0.1:8080/v1/completions
 -H "Content-Type: application/json" -d '{
"model": "local",
"prompt": "Say hello in one short sentence.",
"max_tokens": 64
}'

UE5 plug-in expectation for v1
• Editor setting for runner host/port and model name
• One Blueprint node: QueryLLM(message) → string reply in PIE

Repository layout (initial)
• /Plugin … UE5 C++ plug-in (coming in next commit)
• /Runner … we use llama-cpp-python server; see commands above
• /Schemas … persona.schema.json, persona.example.json, memory.example.json
• /Samples/DemoMap … Guard.persona.json, Merchant.persona.json
• /Scripts … download_model.sh (instructions only)
• /Media … screenshots and a short demo video (not committed if large)

Git hygiene
• Do not commit model weights or large media
• Ensure /models/ is in .gitignore

License
Apache-2.0. See NOTICE and THIRD_PARTY_NOTICES.md.









