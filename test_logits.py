import torch
from evaluate import MuZeroModel
model = MuZeroModel()
model.load_state_dict(torch.load('checkpoints/worker_1/model_iter_594000.pth'), strict=False)
model.eval()
# Create extreme inputs: extreme negative and extreme positive
input_extreme_neg = torch.tensor([[-100.0, -100.0, -100.0, -100.0]])
input_extreme_pos = torch.tensor([[100.0, 100.0, 100.0, 100.0]])
with torch.no_grad():
    _, val_neg = model(input_extreme_neg)
    _, val_pos = model(input_extreme_pos)
print(f'Extreme Neg Value: {val_neg}')
print(f'Extreme Pos Value: {val_pos}')
