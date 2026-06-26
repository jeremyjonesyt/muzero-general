import torch
from src.muzero.mcts.search import run_mcts, get_search_statistics
from src.muzero.mcts.node import Node
from src.muzero.model.representation import RepresentationNetwork
from src.muzero.model.dynamics import DynamicsNetwork
from src.muzero.model.prediction import PredictionNetwork
from src.muzero.training.replay_buffer import ReplayBuffer

class Model:
    def __init__(self):
        self.representation = RepresentationNetwork()
        self.dynamics_net = DynamicsNetwork()
        self.dynamics = self.dynamics_net
        self.prediction_network = PredictionNetwork()
        self.prediction = self.prediction_network

model = Model()
root = Node(prior=0.0)
root.hidden_state = torch.randn(1, 64)
buffer = ReplayBuffer()

# Run Simulation
run_mcts(model, root, num_simulations=10)

# Extract targets using the new function
stats = get_search_statistics(root, action_space_size=5)
print(f"Policy Target: {stats['policy_target']}")
print(f"Value Target: {stats['value_target']}")
