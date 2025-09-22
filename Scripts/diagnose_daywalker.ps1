param(
  [string]$Runner = "http://127.0.0.1:8081",
  [string]$Proxy  = "http://127.0.0.1:8092"
)
Write-Host "Checking runner at $Runner ..." -ForegroundColor Cyan
try {
  $r = Invoke-RestMethod -Uri "$Runner/v1/models" -Method GET -ErrorAction Stop
  Write-Host "Runner OK" -ForegroundColor Green
} catch {
  try {
    $r = Invoke-RestMethod -Uri "$Runner/v1/completions" -Method POST -ContentType 'application/json' -Body '{"model":"local","prompt":"ping","max_tokens":1}' -ErrorAction Stop
    Write-Host "Runner OK (via /v1/completions)" -ForegroundColor Green
  } catch {
    Write-Host "Runner NOT reachable" -ForegroundColor Red
    Write-Host $_
    exit 1
  }
}

Write-Host "Checking proxy at $Proxy ..." -ForegroundColor Cyan
try {
  $p = Invoke-RestMethod -Uri "$Proxy/dev/health" -Method GET -ErrorAction Stop
  if ($p.ok) { Write-Host "Proxy OK" -ForegroundColor Green } else { Write-Host "Proxy up but runner reported offline" -ForegroundColor Yellow }
} catch {
  Write-Host "Proxy NOT reachable" -ForegroundColor Red
  Write-Host $_
  exit 1
}

$q = "How do I save the current level and where are screenshots stored?"
Write-Host "Sample Q/A via proxy: $q" -ForegroundColor Cyan
try {
  $ans = Invoke-RestMethod -Uri "$Proxy/dev/ask" -Method POST -ContentType 'application/json' -Body (@{q=$q} | ConvertTo-Json -Compress)
  if ($ans.ok) {
    Write-Host "Answer:" -ForegroundColor Green
    Write-Host $ans.answer
  } else {
    Write-Host "Proxy returned ok:false -> $($ans.error)" -ForegroundColor Yellow
  }
} catch {
  Write-Host "Proxy call failed:" -ForegroundColor Red
  Write-Host $_
  exit 1
}
