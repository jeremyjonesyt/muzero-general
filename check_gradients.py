import torch
from train import MuZeroModel

model = MuZeroModel(hidden_dim=64, action_dim=5)
# Using a more robust way to select the first layer's weights
first_layer_name = next(iter(model.representation.named_parameters()))[0]
initial_weights = dict(model.representation.named_parameters())[first_layer_name].clone()

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Run a dummy step
dummy_input = torch.randn(1, 4, 64, 64) 
out = model(dummy_input)
loss = out['policy_logits'].sum()
loss.backward()
optimizer.step()

# Check if weights changed
new_weights = dict(model.representation.named_parameters())[first_layer_name].clone()
if torch.equal(initial_weights, new_weights):
    print(f"CRITICAL ERROR: Weights for {first_layer_name} did not change!")
else:
    print(f"Success: Weights for {first_layer_name} updated.")
