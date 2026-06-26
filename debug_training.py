import torch
import torch.nn as nn
import torch.optim as optim
from src.muzero.model.representation import RepresentationNetwork
from src.muzero.model.prediction import PredictionNetwork

# 1. Setup minimal components
hidden_dim = 64
model_pred = PredictionNetwork() # Assuming this outputs policy, value
optimizer = optim.Adam(model_pred.parameters(), lr=0.001)

# 2. Mock inputs
hidden_state = torch.randn(1, hidden_dim, requires_grad=True)
target_policy = torch.tensor([[0.0, 1.0, 0.0, 0.0, 0.0]]) # Goal: Action 1
target_value = torch.tensor([1.0])

# 3. Training step
optimizer.zero_grad()
policy, value = model_pred(hidden_state)
loss = nn.CrossEntropyLoss()(policy, target_policy) + nn.MSELoss()(value, target_value)

loss.backward()

# 4. Inspection
print(f'Loss: {loss.item():.4f}')
print(f'Policy Layer Gradient (Sample): {list(model_pred.parameters())[0].grad.view(-1)[0]}')

if list(model_pred.parameters())[0].grad is not None:
    print('SUCCESS: Gradients are flowing to the Prediction Head.')
else:
    print('FAILURE: No gradients detected. Check your loss function connection.')
