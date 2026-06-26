$env:PYTHONPATH = "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src"
Write-Host "--- Initiating Large Scale Training: 500 Iterations ---" -ForegroundColor Cyan

for ($i = 1; $i -le 500; $i++) {
    Write-Host "Iteration: $i / 500" -ForegroundColor Yellow
    & ".\venv_muzero\Scripts\python.exe" -m muzero.training.inference_loop
    & ".\venv_muzero\Scripts\python.exe" -m muzero.training.train_muzero
    
    # Optional: Periodic validation every 50 iterations
    if ($i % 50 -eq 0) {
        Write-Host "Running periodic validation..." -ForegroundColor Green
        & ".\venv_muzero\Scripts\python.exe" -m muzero.training.test_agent
    }
}
Write-Host "--- Large Scale Training Complete ---" -ForegroundColor Green
