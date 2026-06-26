import torch
import pandas as pd
from muzero.training.orchestrator import TrainingOrchestrator

# Load model/orchestrator
config = {"learning_rate": 5e-4}
orchestrator = TrainingOrchestrator(config)
# orchestrator.load_model('model_weights.pth') # Ensure your path is correct

# Load unseen 2026 data
live_stats = pd.read_csv(r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\season_2026_stats.csv')

# Perform inference
for index, row in live_stats.iterrows():
    observation = torch.tensor([[row['feature1'], row['feature2']]]) # Adjust based on your features
    prediction = orchestrator.predict(observation)
    print(f"Prediction for row {index}: {prediction}")
