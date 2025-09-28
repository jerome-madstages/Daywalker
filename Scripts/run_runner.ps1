param(
  [string]$Model = "D:\Models\tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)
& "$env:USERPROFILE\daywalker-venv\Scripts\Activate.ps1"
python -m llama_cpp.server --model "$Model" --host 127.0.0.1 --port 8081 --n_ctx 2048
