Write-Host "--- MuZero Training Fleet Monitor ---" -ForegroundColor Cyan
$workers = Get-ChildItem -Path ".\checkpoints\worker_*" -Directory
foreach ($worker in $workers) {
    $latest = Get-ChildItem -Path $worker.FullName -Filter "*.pth" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latest) {
        $iteration = $latest.Name.Split('_')[-1].Replace('.pth', '')
        $time = $latest.LastWriteTime.ToString('HH:mm:ss')
        Write-Host "$($worker.Name): Current Iteration: $iteration | Last Update: $time"
    } else {
        Write-Host "$($worker.Name): Initializing..." -ForegroundColor Yellow
    }
}
