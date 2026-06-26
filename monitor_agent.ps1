\.\inference_history.csv = ".\inference_history.csv"
if (Test-Path \.\inference_history.csv) {
    Write-Host "--- MuZero Agent Performance Report ---" -ForegroundColor Cyan
    \          = Import-Csv \.\inference_history.csv | Select-Object -Last 10
    \-0.800655832 = (\          | Measure-Object -Property value_estimate -Average).Average
    Write-Host "Recent Average Value Estimate: \-0.800655832" -ForegroundColor Yellow
    if (\-0.800655832 -gt 0.5) {
        Write-Host "Status: Agent is predicting a win trend." -ForegroundColor Green
    } else {
        Write-Host "Status: Agent is predicting a loss trend." -ForegroundColor Red
    }
} else {
    Write-Host "Log file not found." -ForegroundColor Red
}
