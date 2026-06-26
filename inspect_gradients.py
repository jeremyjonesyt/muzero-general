import torch
import torch.nn as nn
from train import MuZeroModel

def check():
    model = MuZeroModel(hidden_dim=64, action_dim=5)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1) # High LR for testing
    criterion = nn.CrossEntropyLoss()
    
    # Simulate a batch
    input_data = torch.randn(1, 4)
    # Target must be a LongTensor (class index) for CrossEntropyLoss
    targets = torch.tensor([0], dtype=torch.long)
    
    optimizer.zero_grad()
    out = model(input_data)
    
    # Check if policy_logits exist
    if 'policy_logits' not in out:
        print("ERROR: Model output missing 'policy_logits'")
        return

    loss = criterion(out['policy_logits'], targets)
    loss.backward()
    
    # Check for gradients
    has_grad = model.representation.net[0].weight.grad is not None
    print(f"Gradient Flow Check: {'SUCCESS' if has_grad else 'FAILED'}")
    if has_grad:
        print(f"Gradient norm: {model.representation.net[0].weight.grad.norm().item()}")
    else:
        print("CRITICAL: No gradients found! Check for .detach() or disconnected layers.")

if __name__ == '__main__':
    check()
