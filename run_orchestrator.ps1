# ====================================================================
# MASTER MUZERO AUTOMATION ENGINE (WITH CPU THROTTLING & CLOUD BACKUP)
# ====================================================================

# --- Deep Automation Configuration Framework ---
$totalBursts     = 50                # Extended deep production run count
$weightFile      = "./muzero_tripartite_model.pth"
$backupFile      = "./backup_best_model.pth"
$tmpFile         = "./muzero_tripartite_model.pth.tmp"
$logFile         = "./automation_flywheel.log"

# Setup structural variables and core engine baseline
$bestStability   = 342.30            
$pyBinary        = "python"
$consecutiveStalls = 0

# Logger Helper Function Definition
function Log-Telemetry($message, $color = "Gray") {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] $message"
    Write-Host $logLine -ForegroundColor $color
    $logLine | Out-File -FilePath $logFile -Append
}

Clear-Host
Log-Telemetry "====================================================" "Cyan"
Log-Telemetry "[*] LAUNCHING ULTRA-DEEP AUTOMATED MUZERO FLYWHEEL" "Cyan"
Log-Telemetry "[*] Established Baseline Safety Gatekeeper: $bestStability Steps" "Gray"
Log-Telemetry "====================================================" "Cyan"

# --- Master Production Loop ---
for ($burst = 1; $burst -le $totalBursts; $burst++) {
    Log-Telemetry "`n[?] Starting Automated Production Burst $burst/$totalBursts" "Magenta"
    Log-Telemetry "----------------------------------------------------" "Gray"

    # 1. Take a clean safety snapshot of the weights before active training begins
    if (Test-Path $weightFile) {
        Copy-Item -Path $weightFile -Destination $tmpFile -Force
        Log-Telemetry "[+] Pre-flight weight matrix snapshot successfully preserved." "DarkGray"
    }

    # 2. Launch the Master Training Iteration with Resource Limits
    Log-Telemetry "[*] Injecting trajectories & executing neural gradient descent (main.py)..." "Cyan"
    
    # --- POWERSHELL RESOURCE THROTTLING ---
    $env:OMP_NUM_THREADS = "2"
    $env:MKL_NUM_THREADS = "2"
    $env:OPENBLAS_NUM_THREADS = "2"
    $env:VECLIB_MAXIMUM_THREADS = "2"
    $env:NUMEXPR_NUM_THREADS = "2"
    # --------------------------------------

    # Configure background processing constraints and lock directory path
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $pyBinary
    $psi.Arguments = "main.py"
    $psi.WorkingDirectory = (Get-Item .).FullName   # <-- FIX: Forces background task to stay in your current project folder
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $false
    $psi.RedirectStandardError = $false
    
    # Ignite background process and lower priority immediately
    $proc = [System.Diagnostics.Process]::Start($psi)
    $proc.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::Idle
    
    # Wait for completion safely
    $proc.WaitForExit()
    $trainingExitCode = $proc.ExitCode

    if ($trainingExitCode -ne 0) {
        Log-Telemetry "[-] CRITICAL: main.py exited with an error code. Initiating crash recovery protocol..." "Red"
        if (Test-Path $tmpFile) { 
            Copy-Item -Path $tmpFile -Destination $weightFile -Force
            Log-Telemetry "[+] Weights successfully rolled back to safety threshold." "Green"
        }
        Start-Sleep -Seconds 10
        continue
    }

    # 3. Gather Telemetry Metrics via Isolated Evaluation Runtime
    Log-Telemetry "[*] Execution finished cleanly. Gathering telemetry statistics (evaluate.py)..." "Cyan"
    $evalOutput = & $pyBinary "evaluate.py" 2>&1 | Out-String

    # 4. Parse Metrics & Execute Checkpoint Gating Logic
    if ($evalOutput -match "Mean Stability Duration:\s*([0-9.]+)") {
        $currentStability = [double]$Matches[1]
        Log-Telemetry "[+] Telemetry recovered. Measured True Stability: $currentStability Steps" "Green"

        if ($currentStability -gt $bestStability) {
            Log-Telemetry "[***] BREAKTHROUGH PROVEN! Performance surged ($bestStability -> $currentStability)." "Green"
            $bestStability = $currentStability
            $consecutiveStalls = 0
            
            # Flush local files
            Copy-Item -Path $weightFile -Destination $backupFile -Force
            Log-Telemetry "[+] Golden checkpoint securely hard-flushed to disk." "Cyan"

            # --- AUTOMATED CLOUD SYNC ---
            Log-Telemetry "[*] Initializing automated Git commit sequence for breakthrough tracking..." "Cyan"
            & git add . 2>&1
            & git commit -m "Automated Breakthrough Update: Peak Stability reached $currentStability Steps" 2>&1
            & git push origin main 2>&1
            if ($LASTEXITCODE -eq 0) {
                Log-Telemetry "[***] CLOUD SYNCHRONIZATION COMPLETE! Code and weights safely protected off-site." "Green"
            } else {
                Log-Telemetry "[-] Cloud Sync Warning: Git push failed." "Yellow"
            }
        } else {
            $consecutiveStalls++
            Log-Telemetry "[-] Stability ($currentStability) dropped below structural peak ($bestStability)." "Yellow"
            if (Test-Path $tmpFile) {
                Copy-Item -Path $tmpFile -Destination $weightFile -Force
                Log-Telemetry "[+] Network successfully reverted to protected maximum state." "DarkYellow"
            }
        }
    } else {
        Log-Telemetry "[-] Telemetry Parsing Failure: 'Mean Stability Duration' signature not found." "Red"
        if (Test-Path $tmpFile) { Copy-Item -Path $tmpFile -Destination $weightFile -Force }
    }

    # 5. Adaptive Stagnation Handling
    if ($consecutiveStalls -ge 5) {
        Log-Telemetry "[!] System Stagnation Alert: 5 consecutive bursts failed to break the peak." "Yellow"
        $consecutiveStalls = 0
    }
}

Log-Telemetry "`n[+] Full automated deep run completed! Peak Performance Reached: $bestStability Steps." "Green"
