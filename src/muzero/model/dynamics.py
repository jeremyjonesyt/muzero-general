import torch
import torch.nn as nn

class DynamicsNetwork(nn.Module):
    def __init__(self, hidden_dim=64, action_dim=5):
        super().__init__()
        self.action_dim = action_dim
        self.action_encoder = nn.Embedding(action_dim, action_dim)
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )
        self.reward_head = nn.Linear(hidden_dim, 1)

    def forward(self, hidden_state, action):
        # Encode and then squeeze to [1, 5] instead of [1, 1, 5]
        action_encoded = self.action_encoder(action).squeeze(1)
        
        # Now both are [1, 64] and [1, 5], so cat works on dim 1
        x = torch.cat([hidden_state, action_encoded], dim=1)
        
        next_hidden = self.fc(x)
        reward = self.reward_head(next_hidden)
        
        return next_hidden, reward
