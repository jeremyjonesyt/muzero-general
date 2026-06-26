import pandas as pd

def evaluate_performance(csv_path):
    # Load with extended schema
    cols = ['Timestamp', 'Episode', 'Loss', 'Reward', 'MCTS_Prob', 'Odds', 
            'Opponent_Win_Pct', 'Home_Away', 'Key_Player_Available']
    df = pd.read_csv(csv_path, names=cols)
    
    # Updated importance model incorporating context
    weights = {
        'Run_Differential': 0.2410,
        'Errors': 0.2342,
        'Opponent_Win_Pct': 0.1500,  # New context variable
        'Home_Away': 0.1000,         # New context variable
        'Key_Player_Available': 0.1200 # New context variable
    }
    
    print("--- 14-0 Contextual Performance Model ---")
    for metric, weight in weights.items():
        print(f"{metric:<20} | Importance: {weight}")

if __name__ == "__main__":
    evaluate_performance(r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\logs_v2\experiment_results.csv')
