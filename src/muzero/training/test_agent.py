import torch
from muzero.training.inference_loop import MuZeroModelWrapper
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork
from parse_mlb_data import parse_game_to_tensor

model = MuZeroModelWrapper(RepresentationNetwork(), DynamicsNetwork(), PredictionNetwork())
model.load_state_dict(torch.load('model_checkpoint.pth'))
model.eval()

# Use detach().clone() to avoid UserWarning
raw_data = parse_game_to_tensor()
state = torch.as_tensor(raw_data, dtype=torch.float32).unsqueeze(0).detach().clone()

with torch.no_grad():
    hidden, policy_logits, value = model.initial_inference(state)
    action = torch.argmax(policy_logits)
    print(f'Agent chose action: {action.item()} with predicted value: {value.item():.4f}')
