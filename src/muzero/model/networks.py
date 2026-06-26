import torch
import torch.nn as nn

class RepresentationNetwork(nn.Module):
    def __init__(self, obs_dim, hidden_dim):
        super().__init__()
        self.fc = nn.Linear(obs_dim, hidden_dim)
    def forward(self, x): return torch.relu(self.fc(x))

class PredictionNetwork(nn.Module):
    def __init__(self, hidden_dim, action_dim):
        super().__init__()
        self.policy = nn.Linear(hidden_dim, action_dim)
        self.value = nn.Linear(hidden_dim, 1)
    def forward(self, x):
        return self.policy(x), self.value(x)
