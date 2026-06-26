import pandas as pd
import matplotlib.pyplot as plt
import os

log_path = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2\experiment_results.csv'

# Load the file, explicitly stating there is no header row
df = pd.read_csv(log_path, header=None)

# Manually assign columns based on your data output:
# ['timestamp', 'episode', 'loss', 'reward', 'extra1', 'extra2']
df.columns = ['timestamp', 'episode', 'loss', 'reward', 'extra1', 'extra2']

# Calculate moving average
df['moving_avg'] = df['loss'].rolling(window=10).mean()

plt.figure(figsize=(10, 5))
plt.plot(df['episode'], df['loss'], alpha=0.3, label='Raw Loss')
plt.plot(df['episode'], df['moving_avg'], color='red', label='10-Episode Moving Avg')
plt.title('Training Loss Over Time')
plt.xlabel('Episode')
plt.ylabel('Loss')
plt.legend()
plt.show()
