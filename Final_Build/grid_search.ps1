param([int]$hidden_size)

Write-Host "Running Cross-Validation for hidden size: $hidden_size" -ForegroundColor Yellow
python scale_model.py # Helper script to adjust config
./run_experiment.ps1 -experiment_name "GridSearch_Size_$hidden_size"
