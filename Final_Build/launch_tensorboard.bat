@echo off
cd /d "C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build"
call "..\venv_muzero\Scripts\activate.bat"
start http://localhost:6006/
tensorboard --logdir="C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\logs_v2"
pause
