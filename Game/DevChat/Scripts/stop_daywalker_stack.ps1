param(
  [int]$RunnerPort = 8081,
  [int]$ProxyPort  = 8092
)
Write-Host "Stopping runner on port $RunnerPort and proxy on port $ProxyPort..."

# Kill by port helper
function Stop-ByPort($port) {
  $pids = (Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -Expand OwningProcess) | Sort-Object -Unique
  foreach ($pid in $pids) {
    try {
      $p = Get-Process -Id $pid -ErrorAction Stop
      Write-Host "Stopping PID $pid ($($p.ProcessName)) listening on $port"
      Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    } catch {}
  }
}

Stop-ByPort $RunnerPort
Stop-ByPort $ProxyPort

# Also stop common process names just in case
foreach ($name in @("python","uvicorn")) {
  Get-Process -Name $name -ErrorAction SilentlyContinue | ForEach-Object {
    try {
      if ($_.MainWindowTitle -like "*llama_cpp.server*" -or $_.Path -like "*uvicorn*") {
        Write-Host "Stopping $($name) PID $($_.Id) ($($_.MainWindowTitle))"
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
      }
    } catch {}
  }
}
Write-Host "Done."
