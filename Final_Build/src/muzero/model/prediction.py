import torch
import torch.nn as nn

class PredictionNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Shared torso
        self.torso = nn.Linear(10, 10)
        # Policy head
        self.policy_head = nn.Linear(10, 10)
        # Value head
        self.value_head = nn.Linear(10, 1)

    def forward(self, x):
        x = self.torso(x)
        return self.policy_head(x), self.value_head(x)
