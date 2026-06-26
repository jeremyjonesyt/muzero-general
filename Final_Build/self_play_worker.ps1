import sys
import os
import torch
import csv
from datetime import datetime

episode_idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from muzero.training.orchestrator import TrainingOrchestrator

config = {"learning_rate": 1e-3, "batch_size": 32}
orchestrator = TrainingOrchestrator(config)

dummy_observation = torch.randn(1, 10)
target_value = torch.tensor([[0.0]])
target_policy = torch.tensor([[0.0]])

loss, reward = orchestrator.run_full_episode(dummy_observation, target_value, target_policy)
print(f"Episode {episode_idx} completed. Loss: {loss}, Reward: {reward}")

# --- LOGGING ONLY (Checkpointing removed to prevent crash) ---
log_dir = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\logs_v2'
os.makedirs(log_dir, exist_ok=True)
csv_file = os.path.join(log_dir, 'experiment_results.csv')

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), episode_idx, loss, reward, 0.0, 0.0])
