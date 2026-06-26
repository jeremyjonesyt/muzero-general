# Master Orchestrator: Agentic 14-0 Pipeline
Write-Host "Mission Control: Initializing Agentic Pipeline..." -ForegroundColor Yellow

# 1. Agentic Data Capture
Write-Host "Running Playwright Agent for live data..." -ForegroundColor Cyan
python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\env\web_agent_env.py

# 2. Training Execution
python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\training\trainer.py
if ($LASTEXITCODE -ne 0) { Write-Host "Trainer Failed. Aborting pipeline." -ForegroundColor Red; exit }

# 3. Statistical Audit
python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\training\performance_tracker.py

# 4. 14-0 Metric Evaluation
python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\training\metrics_evaluator.py

# 5. Final Reporting
python C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\src\muzero\training\performance_reporter.py

Write-Host "Mission Control: Agentic pipeline complete. All systems nominal." -ForegroundColor Green
