import torch
import numpy as np

class MCTS:
    def __init__(self, model):
        self.model = model

    def run(self, state):
        # Simplified: Select action based on policy head
        hidden = self.model.representation(state)
        policy_logits, _ = self.model.prediction(hidden)
        action = torch.argmax(policy_logits, dim=-1).item()
        return action
