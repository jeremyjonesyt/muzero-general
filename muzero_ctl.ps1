param(
    [Parameter(Mandatory=True)]
    [ValidateSet("train", "monitor", "reset", "edit_config", "plot", "report", "help")]]]
    $command
)

switch ($command) {
    "train" {
        Write-Host "Starting training batch..." -ForegroundColor Cyan
        ./run_session.ps1
    }
    "monitor" {
        Write-Host "Opening training logs..." -ForegroundColor Yellow
        Invoke-Item "logs\experiment_results.csv"
    }
    "edit_config" {
        Write-Host "Opening configuration for editing..." -ForegroundColor Yellow
        notepad config.yaml
    }
    "plot" {
        Write-Host "Generating performance plots..." -ForegroundColor Magenta
        python plot_results.py
    }
    "report" {
        Write-Host "Generating summary report..." -ForegroundColor Green
        python generate_report.py
    }
    "reset" {
        Write-Host "Running master system verification..." -ForegroundColor Green
        ./master_init.ps1
    }
    "help" {
        Write-Host "MuZero v14-0 Controller"
        Write-Host "Usage: ./muzero_ctl.ps1 -command [train|monitor|reset]"
    }
}
