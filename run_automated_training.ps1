Write-Host "Starting Training..." -ForegroundColor Cyan
for ($i=1; $i -le 1000; $i++) {
    python ".\Final_Build\self_play_worker.ps1" $i
}
Write-Host "Training Complete. Running automated analysis..." -ForegroundColor Yellow
python ".\analyze_performance.py"
Write-Host "Pipeline Finished." -ForegroundColor Green
