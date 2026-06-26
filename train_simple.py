import torch
import torch.nn as nn
import torch.optim as optim
from src.muzero.model.representation import RepresentationNetwork
from src.muzero.model.prediction import PredictionNetwork

# 1. Setup
hidden_dim = 64
# Creating a combined model
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.rep = RepresentationNetwork(input_dim=4, hidden_dim=64)
        self.pred = PredictionNetwork()
    def forward(self, x):
        return self.pred(self.rep(x))

model = SimpleNet()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion_policy = nn.CrossEntropyLoss()

# 2. Forced Learning: Teach the model that state [1,0,0,0] -> Action 1
input_state = torch.tensor([[1.0, 0.0, 0.0, 0.0]], dtype=torch.float32)
target_action = torch.tensor([1], dtype=torch.long)

for epoch in range(100):
    optimizer.zero_grad()
    policy, _ = model(input_state)
    
    loss = criterion_policy(policy, target_action)
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f'Epoch {epoch} | Loss: {loss.item():.4f} | Prob for Action 1: {torch.softmax(policy, dim=1)[0][1]:.4f}')
