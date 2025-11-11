# Skrypt PowerShell do łatwego sprawdzania logów
# Użycie: .\check_logs.ps1

Write-Host "=== OSTATNIE 100 LINII LOGÓW BACKEND ===" -ForegroundColor Green
docker compose logs ai-agent-backend --tail=100

Write-Host "`n=== LOGI Z RAG (ostatnie 50) ===" -ForegroundColor Yellow
docker compose logs ai-agent-backend --tail=200 | Select-String -Pattern "RAG|📚|✅|⚠️|❌|Dynamic" | Select-Object -Last 50

Write-Host "`n=== LOGI Z BŁĘDÓW (ostatnie 20) ===" -ForegroundColor Red
docker compose logs ai-agent-backend --tail=200 | Select-String -Pattern "ERROR|❌|Exception|Traceback" | Select-Object -Last 20

