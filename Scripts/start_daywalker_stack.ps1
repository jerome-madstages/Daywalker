param(
  [string]$ModelPath = "D:\Models\mistral-7b-instruct-q4_K_M.gguf",
  [int]$RunnerPort = 8081,
  [int]$ProxyPort  = 8092
)
# Runner
$runnerCmd = "python -m llama_cpp.server --model `"$ModelPath`" --host 127.0.0.1 --port $RunnerPort --n_ctx 4096"
Start-Process powershell -ArgumentList "-NoExit","-Command",$runnerCmd

# Proxy
$proxyFolder = "$env:USERPROFILE\Desktop\Daywalker\DevChat"
$proxyCmd = "cd `"$proxyFolder`"; `$env:RUNNER_URL=`"http://127.0.0.1:$RunnerPort`"; python -m uvicorn devchat_proxy:app --host 127.0.0.1 --port $ProxyPort --reload"
Start-Process powershell -ArgumentList "-NoExit","-Command",$proxyCmd

Write-Host "Launched runner on $RunnerPort and proxy on $ProxyPort" -ForegroundColor Green
