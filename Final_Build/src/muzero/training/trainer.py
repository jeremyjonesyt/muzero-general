import torch
import torch.nn.functional as F
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork

class MuZeroTrainer:
    def __init__(self):
        self.representation = RepresentationNetwork()
        self.dynamics = DynamicsNetwork()
        self.prediction = PredictionNetwork()
        self.optimizer = torch.optim.Adam(
            list(self.representation.parameters()) +
            list(self.dynamics.parameters()) +
            list(self.prediction.parameters())
        )

    def train_step(self, batch):
        self.optimizer.zero_grad()
        
        obs = torch.randn(1, 10)
        state = self.representation(obs)
        
        # Now correctly receiving two outputs
        policy_logits, value = self.prediction(state)
        
        # Targets
        target_policy = torch.randn(1, 10)
        target_value = torch.randn(1, 1)
        
        loss = F.cross_entropy(policy_logits, target_policy) + F.mse_loss(value, target_value)
        
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
