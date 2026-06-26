import torch
import torch.nn as nn

class DynamicsNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(10, 10)

    def forward(self, x):
        return self.net(x)
