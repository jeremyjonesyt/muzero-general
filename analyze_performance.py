import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
results_csv = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2\experiment_results.csv'
season_data = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\season_2026_stats.csv'

# Load training data
df = pd.read_csv(results_csv, header=None, names=['Timestamp', 'Episode', 'Loss', 'Reward', 'MCTS_Prob', 'Odds'])

# 1. Calculate 50-episode Moving Average
df['Moving_Avg'] = df['Loss'].rolling(window=50).mean()

# 2. Plotting the results
plt.figure(figsize=(12, 6))
plt.plot(df['Episode'], df['Loss'], alpha=0.3, label='Raw Loss')
plt.plot(df['Episode'], df['Moving_Avg'], color='red', label='50-Episode Moving Avg')
plt.title('Training Loss Convergence')
plt.xlabel('Episode')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

# 3. Overfitting Check (Simple comparison)
print(f"Final 50-episode Average Loss: {df['Moving_Avg'].iloc[-1]:.4f}")
if os.path.exists(season_data):
    print("Season 2026 data found. Running correlation analysis...")
    # Add your specific comparison logic here
else:
    print("Warning: season_2026_stats.csv not found. Skipping season comparison.")
