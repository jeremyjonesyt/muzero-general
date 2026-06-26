import torch
import torch.nn as nn

class RepresentationNetwork(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=64):
        super().__init__()
        # Changed from high-dimensional image input to match your 4-element dummy state
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, hidden_dim)
        )

    def forward(self, x):
        return self.net(x)
