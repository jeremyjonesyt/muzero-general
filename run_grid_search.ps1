$rates = @('1e-3', '5e-4', '1e-4')
foreach ($rate in $rates) {
    Write-Host "Starting training with LR: $rate" -ForegroundColor Cyan
    # Update config or environment variable here
    .\run_automated_training.ps1
    
    # Move results to specific folder
    Move-Item -Path ".\logs_v2\experiment_results.csv" -Destination ".\logs_v2\results_lr_$rate.csv"
}
Write-Host "Grid search complete." -ForegroundColor Green
