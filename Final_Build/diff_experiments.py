import pandas as pd
import yaml
import os

def run_diff():
    if not os.path.exists('logs/experiment_results.csv'):
        print("No logs found. Run an experiment first.")
        return

    df = pd.read_csv('logs/experiment_results.csv')
    # Group by config state if you expand logging, 
    # for now, we compare the best reward iteration
    best = df.loc[df['reward'].idxmax()]
    
    print("--- Automated Performance Analysis ---")
    print(f"Top Performing Episode: {best['episode']}")
    print(f"Highest Reward: {best['reward']:.4f}")
    print(f"Associated Loss: {best['loss']:.4f}")
    print("---------------------------------------")

if __name__ == '__main__':
    run_diff()
