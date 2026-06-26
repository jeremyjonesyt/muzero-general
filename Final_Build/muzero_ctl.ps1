param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("train", "monitor", "reset", "edit_config", "plot", "report", "inspect", "experiment", "diff", "grid_search", "archive", "monitor_loop", "run_campaign", "help")]
    $command
)

switch ($command) {
    "train" { ./run_session.ps1 }
    "monitor" { Invoke-Item "logs\experiment_results.csv" }
    "reset" { ./master_init.ps1 }
    "edit_config" { notepad config.yaml }
    "plot" { python plot_results.py }
    "report" { python generate_report.py }
    "inspect" { python inspect_model.py }
    "experiment" { ./run_experiment.ps1 -experiment_name "Batch_Tuning_Session" }
    "diff" { python diff_experiments.py }
    "grid_search" { ./grid_search.ps1 -hidden_size 128 }
    "archive" { python checkpoint_manager.py }
    "monitor_loop" { Start-Process powershell -ArgumentList "-Command python continuous_monitor.py" }
    "run_campaign" {
        Write-Host "Executing Master Campaign Orchestrator..." -ForegroundColor Magenta
        ./run_campaign.ps1
    }
    "tensorboard" {
        Write-Host "Launching TensorBoard at http://localhost:6006..." -ForegroundColor Cyan
        Start-Process tensorboard -ArgumentList "--logdir=logs"
    }
    "reset" { ./run_campaign.ps1 }
    "help" { 
        Write-Host "MuZero v14-0 Controller"
        Write-Host "Available commands: train, monitor, reset, edit_config, plot, report, inspect, experiment, diff, grid_search, archive, monitor_loop, run_campaign"
    }
}
