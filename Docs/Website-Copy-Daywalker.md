Daywalker Dev Chat (Pops-lite)

Summary
Unreal-first developer chat that runs locally. The UE Python helper talks to a small proxy on localhost:8092 which relays to a local llama.cpp runner on localhost:8081. No cloud dependency.

What it does today
• Answer Unreal workflow questions from inside the Unreal Editor Python console
• Constrain answers to Unreal/Daywalker scope
• Provide deterministic answers for common tasks via a small UE5 knowledge base
• Offer a simple local web page for quick testing at http://127.0.0.1:8092/devchat

Quickstart
1) Start runner
   python -m llama_cpp.server --model D:\Models\mistral-7b-instruct-q4_K_M.gguf --host 127.0.0.1 --port 8081 --n_ctx 4096
2) Start proxy
   DevChat\start_devchat_proxy.ps1
3) Ask in UE
   import dw_dev
   print(dw_dev.ask("How do I save the current level and where are screenshots stored?"))

Media
• UE Q→A
• Dev Chat page
• Proxy status
• Runner
• Desktop overview

Links
• GitHub repository: jerome-madstages/Daywalker
• See Docs/Quickstart.md, Docs/Troubleshooting.md, Docs/DevChat.md for details
