import torch
import torch.nn as nn
import torch.optim as optim
from src.muzero.model.representation import RepresentationNetwork
from src.muzero.model.prediction import PredictionNetwork

# Simple model wrapper
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.rep = RepresentationNetwork(input_dim=4, hidden_dim=64)
        self.pred = PredictionNetwork()
    def forward(self, x):
        return self.pred(self.rep(x))

model = SimpleModel()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

# Force a simple association: Input [1,0,0,0] MUST result in Action 1
input_data = torch.tensor([[1.0, 0.0, 0.0, 0.0]], dtype=torch.float32)
target = torch.tensor([1], dtype=torch.long)

print('--- Starting Sanity Check ---')
for epoch in range(101):
    optimizer.zero_grad()
    policy, _ = model(input_data)
    loss = criterion(policy, target)
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        probs = torch.softmax(policy, dim=1)
        print(f'Epoch {epoch} | Loss: {loss.item():.4f} | Action 1 Prob: {probs[0][1]:.4f}')
