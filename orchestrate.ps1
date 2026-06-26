# ====================================================================
#          MUZERO PRODUCTION AUTOMATION & TELEMETRY ENGINE
# ====================================================================

$ModelPath = ".\muzero_tripartite_model.pth"
$MainScript = ".\main.py"
$LogPath = ".\flywheel_output.log"

# 1. Clean up stale architecture states
if (Test-Path $LogPath) { Remove-Item $LogPath -ErrorAction Ignore }
if (Test-Path $ModelPath) { Remove-Item $ModelPath -ErrorAction Ignore }

Clear-Host
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "     LAUNCHING HIGH-FIDELITY MCTS FLYWHEEL ENGINE    " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 2. Spawn the background worker with live stream routing
Write-Host "[*] Spawning MuZero optimization subprocess..." -ForegroundColor Yellow
Start-Process python -ArgumentList $MainScript -RedirectStandardOutput $LogPath -NoNewWindow

# Wait briefly for standard file streams to bind
Start-Sleep -Seconds 3

# 3. Telemetry Watchdog Loop
while ($true) {
    Clear-Host
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host "         MUZERO SYSTEM AUTOMATION CONSOLE           " -ForegroundColor Cyan
    Write-Host "====================================================" -ForegroundColor Cyan

    if (Test-Path $ModelPath) {
        $File = Get-Item $ModelPath
        $LastUpdate = $File.LastWriteTime
        $SizeKB = [math]::Round(($File.Length / 1KB), 2)
        $TimePassed = (Get-Date) - $LastUpdate

        $Color = "Green"
        if ($TimePassed.TotalSeconds -gt 45) { $Color = "Yellow" }
        if ($TimePassed.TotalSeconds -gt 120) { $Color = "Red" }

        Write-Host "[+] Engine Status: UNLOCKED & ACTIVE" -ForegroundColor Green
        Write-Host " -> Current Network Weights: $SizeKB KB" -ForegroundColor Gray
        Write-Host " -> Last Weight Export:      $($LastUpdate.ToString('HH:mm:ss'))" -ForegroundColor Gray
        Write-Host " -> Time Since Optimization: [ $([math]::Round($TimePassed.TotalSeconds, 1)) s ]" -ForegroundColor $Color
    } else {
        Write-Host "[*] Engine Status: INITIALIZING EXPERT SEED HOOD..." -ForegroundColor Yellow
        Write-Host " -> Parsing raw observations and running heuristic lookaheads..." -ForegroundColor Gray
    }

    # Stream the tail-end of real MCTS search trajectories live to screen
    Write-Host "`n--- LIVE SUBPROCESS OUTPUT TRAIL ---" -ForegroundColor DarkCyan
    if (Test-Path $LogPath) {
        Get-Content $LogPath -Tail 10 | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }
    }

    Write-Host "`n[Control + C] to terminate orchestrator loop." -ForegroundColor DarkGray
    Start-Sleep -Seconds 3
}
