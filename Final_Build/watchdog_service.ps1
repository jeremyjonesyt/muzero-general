Write-Host "--- 14-0 Watchdog Active: Monitoring Queue ---" -ForegroundColor Yellow

$folder = "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\queue"
$filter = "*.json"

$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $folder
$watcher.Filter = $filter
$watcher.IncludeSubdirectories = $false
$watcher.EnableRaisingEvents = $true

$action = {
    $path = $Event.SourceEventArgs.FullPath
    Write-Host "New data detected: $path. Launching 14-0 Pipeline..." -ForegroundColor Cyan
    powershell -ExecutionPolicy Bypass -File "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\bootstrap.ps1"
}

Register-ObjectEvent $watcher "Created" -Action $action

while ($true) { Start-Sleep -Seconds 1 }
