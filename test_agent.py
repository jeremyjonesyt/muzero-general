import torch
from src.muzero.model.representation import RepresentationNetwork
from src.muzero.model.dynamics import DynamicsNetwork
from src.muzero.model.prediction import PredictionNetwork
from train import MuZeroModel
from src.muzero.mcts import MCTS

# Dummy Env
class DummyEnv:
    def reset(self): return [0.0, 0.0, 0.0, 0.0]
    def step(self, action): return [0.0, 0.0, 0.0, 0.0], 1.0, True, {}

model = MuZeroModel(hidden_dim=64, action_dim=5)
mcts = MCTS(model)
env = DummyEnv()

# Verify MCTS run
initial_state = model.representation(torch.randn(1, 4))
action = mcts.run(initial_state)
print(f"Test Successful: Agent selected action {action}")
