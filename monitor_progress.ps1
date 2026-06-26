\ = Import-Csv ".\data\system_records.csv"
\ = Import-Csv ".\data\Performance_History.csv"

Write-Host "
--- SYSTEM LEARNING MONITOR ---" -ForegroundColor Yellow
Write-Host "Total Automated Runs: " + (\.Count) -ForegroundColor Cyan
Write-Host "Last Run: " + (\[-1].Timestamp) -ForegroundColor Green

Write-Host "
--- RECENT PERFORMANCE METRICS ---" -ForegroundColor Yellow
\ | Select-Object -Last 5 | Format-Table -AutoSize
