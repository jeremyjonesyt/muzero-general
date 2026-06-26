import torch
import torch.nn as nn
import torch.nn.functional as F

class RepresentationNetwork(nn.Module):
    """Encodes raw observations into an internal hidden/latent state representation."""
    def __init__(self, input_dim=4, hidden_dim=256):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, obs):
        x = F.relu(self.fc1(obs))
        hidden_state = torch.tanh(self.fc2(x))  # Normalize hidden space bound
        return hidden_state

class DynamicsNetwork(nn.Module):
    """Simulates internal transitions: (hidden_state, action) -> (next_hidden_state, reward)."""
    def __init__(self, hidden_dim=256, action_dim=4):
        super().__init__()
        # Input to fc1 is combined size of hidden state vector + action scalar space
        self.fc1 = nn.Linear(hidden_dim + action_dim, hidden_dim)
        self.fc_state = nn.Linear(hidden_dim, hidden_dim)
        self.fc_reward = nn.Linear(hidden_dim, 1)

    def forward(self, hidden_state, action_one_hot):
        # Concatenate current hidden state vector and the one-hot action vector
        combined = torch.cat([hidden_state, action_one_hot], dim=-1)
        x = F.relu(self.fc1(combined))
        
        next_hidden_state = torch.tanh(self.fc_state(x))
        reward = self.fc_reward(x)
        return next_hidden_state, reward

class PredictionNetwork(nn.Module):
    """Predicts policy priorities and value estimates given a hidden state."""
    def __init__(self, hidden_dim=256, action_dim=4):
        super().__init__()
        self.fc1 = nn.Linear(hidden_dim, hidden_dim)
        self.fc_policy = nn.Linear(hidden_dim, action_dim)
        self.fc_value = nn.Linear(hidden_dim, 1)

    def forward(self, hidden_state):
        x = F.relu(self.fc1(hidden_state))
        policy_logits = self.fc_policy(x)
        policy_probs = F.softmax(policy_logits, dim=-1)
        value = self.fc_value(x)
        return policy_probs, value

class CompleteMuZeroNet(nn.Module):
    """Ties all three networks together into a single unified MuZero model interface."""
    def __init__(self, input_dim=4, action_dim=4, hidden_dim=256):
        super().__init__()
        self.action_dim = action_dim
        self.representation = RepresentationNetwork(input_dim, hidden_dim)
        self.dynamics = DynamicsNetwork(hidden_dim, action_dim)
        self.prediction = PredictionNetwork(hidden_dim, action_dim)

    def initial_inference(self, obs):
        """Used at the root of MCTS: raw observation -> policy & value."""
        hidden_state = self.representation(obs)
        policy_probs, value = self.prediction(hidden_state)
        return hidden_state, policy_probs, value

    def recurrent_inference(self, hidden_state, action):
        """Used down the MCTS tree blocks: (hidden_state, action) -> (next_hidden_state, reward, policy, value)."""
        # Convert action vector indexes directly to one-hot on inference fly
        action_one_hot = F.one_hot(action.long(), num_classes=self.action_dim).float()
        next_hidden_state, reward = self.dynamics(hidden_state, action_one_hot)
        policy_probs, value = self.prediction(next_hidden_state)
        return next_hidden_state, reward, policy_probs, value

if __name__ == "__main__":
    print("[+] Instantiating Complete Tripartite MuZero Network...")
    model = CompleteMuZeroNet(input_dim=4, action_dim=4, hidden_dim=256)
    
    # Simple evaluation sanity verification check
    dummy_raw_obs = torch.randn(1, 4)
    h_state, p, v = model.initial_inference(dummy_raw_obs)
    print(f"[+] Initial Inference -> Latent State Shape: {list(h_state.shape)} | Value: {v.item():.4f}")
    
    dummy_action = torch.tensor([1])
    next_h, r, next_p, next_v = model.recurrent_inference(h_state, dummy_action)
    print(f"[+] Recurrent Inference -> Next Latent State Shape: {list(next_h.shape)} | Reward: {r.item():.4f}")
    print("[+] Triple-net functional testing check completed successfully!")

