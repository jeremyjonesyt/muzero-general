import pandas as pd
import time
import os
import subprocess

def monitor_and_archive():
    last_best_reward = -float('inf')
    log_file = 'logs/experiment_results.csv'
    
    print("Monitor active: Watching for new reward milestones...")
    
    while True:
        if os.path.exists(log_file):
            df = pd.read_csv(log_file)
            current_best = df['reward'].max()
            
            if current_best > last_best_reward:
                print(f"New milestone detected: {current_best:.4f}. Archiving...")
                subprocess.run(['./muzero_ctl.ps1', '-command', 'archive'])
                last_best_reward = current_best
        
        time.sleep(60) # Poll every minute

if __name__ == '__main__':
    monitor_and_archive()
