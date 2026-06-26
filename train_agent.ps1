Write-Host "--- Starting Autonomous Training Loop ---" -ForegroundColor Cyan
for ($i = 1; $i -le 50; $i++) {
    Write-Host "Iteration: $i / 50" -ForegroundColor Yellow
    & ".\venv_muzero\Scripts\python.exe" -m muzero.training.inference_loop
    & ".\venv_muzero\Scripts\python.exe" -m muzero.training.train_muzero
}
Write-Host "--- Training Complete ---" -ForegroundColor Green
