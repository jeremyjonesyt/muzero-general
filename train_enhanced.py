import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np

# --- Configuration ---
EPSILON_START = 1.0
EPSILON_END = 0.1
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001

class Trainer:
    def __init__(self, model):
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
        self.epsilon = EPSILON_START

    def get_action(self, state, action_dim):
        # Epsilon-Greedy Strategy
        if random.random() < self.epsilon:
            return random.randint(0, action_dim - 1)
        else:
            with torch.no_grad():
                policy, _ = self.model(state)
                return torch.argmax(policy, dim=1).item()

    def update_epsilon(self):
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

    def train_step(self, batch):
        # batch structure: states, target_policies, target_values
        states, target_policies, target_values = batch
        
        self.optimizer.zero_grad()
        policy, value = self.model(states)
        
        # Calculate losses
        policy_loss = nn.CrossEntropyLoss()(policy, target_policies)
        value_loss = nn.MSELoss()(value, target_values)
        total_loss = policy_loss + value_loss
        
        total_loss.backward()
        self.optimizer.step()
        
        return total_loss.item()

print('Enhanced Training Controller Ready.')
print(f'Strategy: Epsilon-Greedy (Starts at {EPSILON_START}, decays to {EPSILON_END})')
