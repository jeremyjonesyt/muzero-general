from models import CompleteMuZeroNet  # Overrides local mismatched definitions
import gymnasium as gym
import torch
import torch.nn as nn
import numpy as np
import os

# ====================================================
#              MUZERO CORE ARCHITECTURE
# ====================================================
class RepresentationNetwork(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=64):
        super().__init__()
        self.layer = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
    def forward(self, obs):
        return self.layer(obs)

class PredictionNetwork(nn.Module):
    def __init__(self, hidden_dim=64, action_dim=2):
        super().__init__()
        self.policy_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )
        self.value_head = nn.Linear(hidden_dim, 1)
        
    def forward(self, hidden_state):
        policy_logits = self.policy_head(hidden_state)
        value = self.value_head(hidden_state)
        return policy_logits, value

class CompleteMuZeroPolicy(nn.Module):
    def __init__(self, obs_dim=4, hidden_dim=64, action_dim=2):
        super().__init__()
        self.representation = RepresentationNetwork(obs_dim, hidden_dim)
        self.prediction = PredictionNetwork(hidden_dim, action_dim)

# ====================================================
#              POLICY EVALUATOR ENGINE
# ====================================================
class MuZeroPolicyEvaluator:
    def __init__(self, checkpoint_path="muzero_tripartite_model.pth"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = CompleteMuZeroNet(input_dim=4, action_dim=2, hidden_dim=64).to(self.device)
        self.model.eval()
        self.loaded = False
        
        if os.path.exists(checkpoint_path):
            try:
                checkpoint = torch.load(checkpoint_path, map_location=self.device)
                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    self.model.load_state_dict(checkpoint["model_state_dict"])
                else:
                    self.model.load_state_dict(checkpoint)
                print("[*] Successfully bound live networks to active hardware target.")
                self.loaded = True
            except Exception as e:
                print(f"[!] Target state map detected mismatch: {e}")
                self.loaded = False
        else:
            print(f"[!] Checkpoint missing at {checkpoint_path}. Operating on fallback mode.")
            self.loaded = False

    def select_action(self, observation):
        if not self.loaded:
            return np.random.choice([0, 1])
        
        with torch.no_grad():
            obs_tensor = torch.FloatTensor(observation).unsqueeze(0).to(self.device)
            hidden_state = self.model.representation(obs_tensor)
            policy_logits, _ = self.model.prediction(hidden_state)
            action = torch.argmax(policy_logits, dim=1).item()
            return action

def evaluate_model(episodes=10):
    try:
        env = gym.make("CartPole-v1")
    except:
        env = gym.make("CartPole-v0")

    policy = MuZeroPolicyEvaluator("muzero_tripartite_model.pth")
    total_steps = 0

    for ep in range(episodes):
        obs, info = env.reset()
        done = False
        truncated = False
        steps = 0
        while not (done or truncated) and steps < 500:
            action = policy.select_action(obs)
            obs, reward, done, truncated, info = env.step(action)
            steps += 1
        total_steps += steps

    mean_stability = total_steps / episodes
    print(f"Mean Stability Duration: {mean_stability:.2f} Steps")

if __name__ == "__main__":
    evaluate_model()
