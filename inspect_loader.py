import torch
import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

from src.muzero.data.loader import MuZeroDataLoader
from train import MuZeroModel

# Initialize
model = MuZeroModel(hidden_dim=64, action_dim=5)
loader = MuZeroDataLoader(model, batch_size=1)

# Sample once
try:
    input_data, targets = loader.sample_batch()
    print(f"--- Data Successfully Loaded ---")
    print(f"Type of targets object: {type(targets)}")
    print(f"Content of targets: {targets}")
except Exception as e:
    print(f"An error occurred during sampling: {e}")
