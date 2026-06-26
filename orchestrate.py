import os
import subprocess
import re
import shutil
import sys

weight_file = "./muzero_tripartite_model.pth"
backup_file = "./checkpoint_perfect_14_52.pth"
tmp_file = "./muzero_tripartite_model.pth.tmp"
best_stability = 0.0
max_bursts = 5

py_binary = sys.executable
# Capture the exact environment mapping currently holding our venv site-packages
current_env = os.environ.copy()

print(f"[*] Subprocess Engine Hardlocked To: {py_binary}")
print("[*] Environment variables captured and passed downstream.")
print("====================================================")
print("   LAUNCHING NATIVE PYTHON MUZERO ORCHESTRATOR      ")
print("====================================================")

for burst in range(1, max_bursts + 1):
    print(f"\n[?] Starting Stabilized Burst {burst}/{max_bursts}")
    print("----------------------------------------------------")
    
    if os.path.exists(weight_file):
        shutil.copyfile(weight_file, tmp_file)
        
    # Run optimization burst passing the explicit environment block
    train_res = subprocess.run([py_binary, "main.py"], env=current_env)
    if train_res.returncode != 0:
        print("[-] Main training loop crashed. Halting orchestrator.")
        break
        
    print("[*] Gathering telemetry statistics...")
    # Evaluate passing the explicit environment block
    eval_res = subprocess.run([py_binary, "evaluate.py"], capture_output=True, text=True, env=current_env)
    eval_output = eval_res.stdout + eval_res.stderr
    
    match = re.search(r"Mean Stability Duration:\s*([0-9.]+)", eval_output)
    if match:
        current_stability = float(match.group(1))
        print(f"[+] Burst {burst} Completed. Current Stability: {current_stability} Steps")
        
        if current_stability >= best_stability:
            best_stability = current_stability
            if os.path.exists(weight_file):
                shutil.copyfile(weight_file, backup_file)
                print("[?] Improved stability horizon verified. Saved backup.")
        else:
            print(f"[!] Divergence detected! Drop from {best_stability} to {current_stability}.")
            if os.path.exists(tmp_file):
                shutil.copyfile(tmp_file, weight_file)
                print("[+] Rollback sequence complete. Restored baseline stable representation weights.")
            break
    else:
        print("[!] Unable to parse evaluation data stream. Stdout/Stderr dump:")
        print(eval_output)
        break

if os.path.exists(tmp_file):
    os.remove(tmp_file)
