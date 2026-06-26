import torch
import torch.nn.functional as F
import pandas as pd
from src.muzero.training.orchestrator import TrainingOrchestrator

class InferenceEngine:
    def __init__(self, model_path, config):
        self.orchestrator = TrainingOrchestrator(config)
        self.load_model(model_path)

    def load_model(self, model_path):
        checkpoint = torch.load(model_path, map_location='cpu')
        self.orchestrator.trainer.representation.load_state_dict(checkpoint, strict=False)
        self.orchestrator.trainer.prediction.load_state_dict(checkpoint, strict=False)
        self.orchestrator.trainer.representation.eval()
        self.orchestrator.trainer.prediction.eval()

    def run_inference(self, data_path, output_path):
        data = pd.read_csv(data_path)
        results = []
        for index, row in data.iterrows():
            # Pad features to 10 (as required by model architecture)
            raw = torch.tensor([row['Loss'], row['Reward']], dtype=torch.float32)
            obs = F.pad(raw, (0, 8), value=0).unsqueeze(0)
            
            state = self.orchestrator.trainer.representation(obs)
            pred = self.orchestrator.trainer.prediction(state)
            results.append({'row': index, 'prediction': pred.item()})
            
        pd.DataFrame(results).to_csv(output_path, index=False)
