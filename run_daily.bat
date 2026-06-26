@echo off
cd /d C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system
call .\venv_muzero\Scripts\activate.bat
python run_mission.py >> mission_log.txt 2>&1
