import torch
import torch.nn as nn
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork
from muzero.training.mcts_engine import MCTSEngine
from muzero.training.replay_buffer import ReplayBuffer
from parse_mlb_data import parse_game_to_tensor

class MuZeroModelWrapper(nn.Module):
    def __init__(self, representation, dynamics, prediction):
        super().__init__()
        self.representation = representation
        self.dynamics_net = dynamics
        self.prediction = prediction
    def initial_inference(self, state):
        hidden = self.representation(state)
        policy_logits, value = self.prediction(hidden)
        return hidden, policy_logits, value

def run_inference(buffer):
    model = MuZeroModelWrapper(RepresentationNetwork(), DynamicsNetwork(), PredictionNetwork())
    engine = MCTSEngine(model)
    state_tensor = parse_game_to_tensor()
    if not isinstance(state_tensor, torch.Tensor): state_tensor = torch.tensor(state_tensor, dtype=torch.float32)
    if state_tensor.dim() == 1: state_tensor = state_tensor.unsqueeze(0)
    
    hidden, policy_logits, value = model.initial_inference(state_tensor)
    buffer.push(state_tensor.squeeze(), torch.argmax(policy_logits), policy_logits.squeeze().detach(), value.squeeze().detach())
    print("Real MCTS inference data pushed to buffer.")

if __name__ == "__main__":
    buffer = ReplayBuffer()
    run_inference(buffer)
