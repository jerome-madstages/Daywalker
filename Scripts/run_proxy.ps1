Set-Location "$env:USERPROFILE\Desktop\Daywalker\DevChat"
$env:RUNNER_URL = "http://127.0.0.1:8081"
# Use plain (no --reload) so editing kb_*.jsonl won't bounce the server
python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port 8092
