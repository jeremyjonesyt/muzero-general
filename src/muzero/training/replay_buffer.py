import pickle
import random

class ReplayBuffer:
    def __init__(self, buffer_size=1000):
        self.buffer = []
        self.max_size = buffer_size

    def save_to_disk(self, filename='buffer.pkl'):
        with open(filename, 'wb') as f: pickle.dump(self.buffer, f)

    def load_from_disk(self, filename='buffer.pkl'):
        try:
            with open(filename, 'rb') as f: self.buffer = pickle.load(f)
        except FileNotFoundError: pass

    def save_game(self, history):
        self.buffer.append(history)
        if len(self.buffer) > self.max_size: self.buffer.pop(0)

    def sample_batch(self, batch_size=32):
        if len(self.buffer) == 0: return None
        return [random.choice(random.choice(self.buffer)) for _ in range(batch_size)]
