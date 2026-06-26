import torch
import torch.nn as nn

class MuZeroModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 5 inputs: away_id, home_id, home_adv, away_streak, home_streak
        self.representation = nn.Linear(5, 16) 
        self.policy = nn.Linear(16, 3)
        self.value = nn.Linear(16, 1)

    def initial_inference(self, x):
        hidden = torch.relu(self.representation(x))
        return hidden, self.policy(hidden), self.value(hidden)
