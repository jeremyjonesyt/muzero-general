$workDir = "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system"
Set-Location -Path $workDir

Write-Host "Triggering MuZero Prediction & Learning Pipeline..." -ForegroundColor Cyan

# 1. Execute the Reinforcement Learning Engine
python train_model_on_rewards.py 

# 2. Automatically log the session
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path ".\data\system_records.csv" -Value "$timestamp,SYSTEM_AUTO_RUN,SUCCESS"

Write-Host "
--- WORKFLOW COMPLETE: SYSTEM STATUS ---" -ForegroundColor Green
$records = Import-Csv ".\data\system_records.csv"
$perf = Import-Csv ".\data\Performance_History.csv"
Write-Host "Total Automated Runs: " + ($records.Count) -ForegroundColor Cyan
Write-Host "Most Recent Metrics:" -ForegroundColor Yellow
$perf | Select-Object -Last 5 | Format-Table -AutoSize
Start-Sleep -Seconds 10
