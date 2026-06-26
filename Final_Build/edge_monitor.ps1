$logDir = 'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2'
$latestLog = Get-ChildItem $logDir -Filter '*.log' | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($latestLog) {
    $matches = Select-String -Path $latestLog.FullName -Pattern 'HIGH_CONFIDENCE_EDGE' -CaseSensitive
    if ($matches) {
        Write-Host "ALERT: High-Confidence Edge Detected in " -ForegroundColor Yellow
        $matches | ForEach-Object { Write-Host $_.Line }
    }
}
