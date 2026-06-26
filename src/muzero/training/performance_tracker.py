import pandas as pd

def check_performance_drift(current_csv, history_csv):
    cols = ['Timestamp', 'Episode', 'Loss', 'Reward', 'MCTS_Prob', 'Odds', 'Opponent_Win_Pct', 'Home_Away', 'Key_Player_Available']
    curr_df = pd.read_csv(current_csv, names=cols, header=None).tail(1)
    
    # We use a simple mean for the history baseline
    hist_df = pd.read_csv(history_csv)
    
    # Check drift for Loss and Reward
    for metric in ['Loss', 'Reward']:
        current_val = float(curr_df[metric].values[0])
        baseline_val = hist_df[metric].mean()
        
        # Avoid division by zero
        if baseline_val != 0:
            drift = abs((current_val - baseline_val) / baseline_val)
            if drift > 0.10:
                print(f"ALERT: {metric} drifted by {drift:.2%}. Review required!")
            else:
                print(f"{metric} within acceptable range (Drift: {drift:.2%}).")

if __name__ == "__main__":
    check_performance_drift(r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\logs_v2\experiment_results.csv',
                            r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\season_2026_stats.csv')
