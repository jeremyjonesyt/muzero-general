import sys
import os
# Ensure the source directory is in the path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from muzero.training.inference_engine import InferenceEngine

# Configuration
config = {"learning_rate": 1e-4}
model_file = 'best_model.pth'
input_data = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\season_2026_stats.csv'
output_data = 'season_2026_predictions.csv'

# Execute via Engine
engine = InferenceEngine(model_file, config)
#engine.run_inference(input_data, output_data)

print(f"Inference Pipeline Automated. Results saved to {output_data}")
