import os
import time
import subprocess
import sys
import parse_mlb_data
import model_inference
import loss_monitor

def check_for_convergence(cycle):
    current_loss = loss_monitor.get_latest_loss()
    print(f'[DEBUG] Current Model Loss: {current_loss}')
    # Stop if loss is below 0.05 OR we exceed 100 cycles
    if current_loss < 0.05 or cycle >= 100:
        return True
    return False

def main():
    cycle_count = 1
    
    print('[DEBUG] Starting training pipeline with loss-based convergence...')
    
    while True:
        timestamp = time.strftime('%H:%M:%S')
        print(f"\n[{timestamp}] --- CYCLE #{cycle_count} STARTING ---")
        
        subprocess.run([sys.executable, "fetch_live_data.py"], check=True)
        tensors = parse_mlb_data.parse_game_to_tensor()
        policy, value = model_inference.run_inference(tensors)
        
        if check_for_convergence(cycle_count):
            print(f"[{timestamp}] [SUCCESS] Model converged/limit reached. Stopping.")
            break
            
        cycle_count += 1
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[SYSTEM SHUTDOWN] Pipeline terminated.")
