\ = 'training.py'

if (Test-Path \) {
    \ = Get-Content \ -Raw
    Write-Host "--- Searching for CrossEntropyLoss/cross_entropy in training.py ---" -ForegroundColor Cyan
    
    # Check if the code uses index [1] to pull targets
    if (\ -match "\[1\]") {
        Write-Host "[SUCCESS] Found index [1] in your training file." -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Could not find index [1] in your training file. This is likely why the loss is stuck." -ForegroundColor Yellow
    }

    # Print relevant lines
    \ -split "
" | Select-String "cross_entropy" | ForEach-Object { Write-Host "Found: \" -ForegroundColor White }
} else {
    Write-Host "training.py not found. Please ensure you are in the current directory." -ForegroundColor Red
}
