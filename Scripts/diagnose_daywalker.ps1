param()
Write-Host "=== Daywalker Diagnostics ===" -ForegroundColor Cyan

# Check runner (8081) and proxy (8092)
function Ping-Json($url) {
  try {
    return Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 3
  } catch { return @{ ok = $false; error = $_.Exception.Message } }
}

$runner  = Ping-Json "http://127.0.0.1:8081/health"  # llama.cpp server often responds 404; this is just a ping
$proxy   = Ping-Json "http://127.0.0.1:8092/dev/health"

"Runner: $($runner | Out-String)"
"Proxy:  $($proxy  | Out-String)"

# Attempt a KB question if proxy ok
if ($proxy.ok) {
  $r = Invoke-RestMethod -Uri http://127.0.0.1:8092/dev/ask -Method POST -ContentType 'application/json' -Body '{"q":"How do I open the Output Log?"}' -ErrorAction SilentlyContinue
  "Ask sample: $($r | Out-String)"
}

# Summarize
if ($proxy.ok) { Write-Host "Proxy OK" -ForegroundColor Green } else { Write-Host "Proxy NOT OK" -ForegroundColor Red }
