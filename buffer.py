import random
from collections import deque
import torch

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state):
        self.buffer.append((state, action, reward, next_state))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states = zip(*batch)
        return torch.cat(states), torch.tensor(actions), torch.tensor(rewards, dtype=torch.float32), torch.cat(next_states)
