import torch.nn as nn

class PredictionNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        # Change this input size from 10 to 64 to match the Representation output
        self.torso = nn.Linear(64, 64) 
        self.policy_head = nn.Linear(64, 5)
        self.value_head = nn.Linear(64, 1)
    
    def forward(self, x):
        x = self.torso(x)
        return self.policy_head(x), self.value_head(x)
