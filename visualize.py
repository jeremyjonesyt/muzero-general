import pandas as pd
import matplotlib.pyplot as plt
import os

# Updated to look inside the Final_Build directory matching your source scripts
log_path = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\logs_v2\experiment_results.csv'

if not os.path.exists(log_path):
    print(f"Error: Target log not found at {log_path}")
else:
    df = pd.read_csv(log_path, header=None, names=['Timestamp', 'Episode', 'Loss', 'Reward', 'MCTS_Prob', 'Odds'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['Episode'], df['Loss'], marker='o', linestyle='-', label='Loss')
    plt.title('MuZero Training Loss Over Time')
    plt.xlabel('Episode')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()
    plt.show()
