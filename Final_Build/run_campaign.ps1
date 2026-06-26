# Master Campaign Orchestrator
# Automates the startup sequence for a full research cycle
Write-Host "--- Launching Autonomous Research Campaign ---" -ForegroundColor Magenta

# 1. Initialize Autonomous Oversight
Write-Host "Starting Background Monitor..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-Command python continuous_monitor.py"

# 2. Launch Scientific Campaign
Write-Host "Initiating Grid Search..." -ForegroundColor Yellow
./grid_search.ps1 -hidden_size 128

Write-Host "--- Campaign Initiated. All systems running. ---" -ForegroundColor Green
