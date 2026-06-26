import sys
import subprocess
import time
import parse_mlb_data
import model_inference

def run_daily_update():
    subprocess.run([sys.executable, "fetch_live_data.py"], check=True)

def main():
    print("============================================================")
    print(" MUZERO MISSION CONTROL: RUNNING CONTINUOUS MLB LOOP")
    print("============================================================")
    
    while True:
        try:
            # 1. Fetch live scoreboard/game state data
            run_daily_update()
            
            # 2. Convert raw data into new game tensors
            game_tensors = parse_mlb_data.parse_game_to_tensor()
            
            if game_tensors is not None:
                # 3. Step the model weights or run live MCTS inference
                policy, value = model_inference.run_inference(game_tensors)
            else:
                print("No fresh game tensors generated. Waiting...")
                
        except Exception as e:
            print(f"Loop Exception caught: {e}")
            
        # Cooldown period (e.g., 30 seconds) before checking for the next play/game update
        print("Awaiting next data cycle...")
        time.sleep(30)

if __name__ == '__main__':
    main()
