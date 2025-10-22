# Stop Flutter processes
Write-Host "Zamykam procesy Flutter..." -ForegroundColor Yellow

$flutterProcesses = Get-Process | Where-Object {$_.ProcessName -like "*flutter*" -or $_.ProcessName -like "*dart*"}

if ($flutterProcesses) {
    foreach ($process in $flutterProcesses) {
        Write-Host "Zamykam proces: $($process.ProcessName) (ID: $($process.Id))" -ForegroundColor Red
        Stop-Process -Id $process.Id -Force
    }
    Write-Host "Wszystkie procesy Flutter zamknięte!" -ForegroundColor Green
} else {
    Write-Host "Brak procesów Flutter do zamknięcia." -ForegroundColor Green
}

# Check if port 3000 is free
$port3000 = netstat -ano | findstr ":3000"
if ($port3000) {
    Write-Host "Port 3000 nadal zajęty:" -ForegroundColor Yellow
    Write-Host $port3000
} else {
    Write-Host "Port 3000 jest wolny!" -ForegroundColor Green
}
