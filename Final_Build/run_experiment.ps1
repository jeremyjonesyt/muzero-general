# Automated Experiment Orchestrator
param([string]$experiment_name)

Write-Host "--- Starting Experiment: $experiment_name ---" -ForegroundColor Yellow
./muzero_ctl.ps1 -command train
./muzero_ctl.ps1 -command report
./muzero_ctl.ps1 -command plot
Write-Host "--- Experiment $experiment_name Complete ---" -ForegroundColor Green
