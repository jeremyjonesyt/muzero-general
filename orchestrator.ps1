\ = 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\system_log.txt'
Add-Content -Path \ -Value "$(Get-Date): Orchestrator cycle started."

# 1. Learn from yesterday's results
& 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\venv_muzero\Scripts\python.exe' 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\train_model_on_rewards.py'

# 2. Hydrate today's data
& 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\venv_muzero\Scripts\python.exe' 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\hydrate_stats.py'

# 3. Predict today's games
& 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\venv_muzero\Scripts\python.exe' 'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\fetch_and_predict.py'

Add-Content -Path \ -Value "$(Get-Date): Orchestrator cycle completed."
