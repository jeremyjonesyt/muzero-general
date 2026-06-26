import torch
import torch.nn.functional as F
import numpy as np

optimizer = None

def run_bptt(model, batch):
    global optimizer
    if optimizer is None:
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # 1. Convert to numpy first, then to tensor for performance
    obs_batch = torch.tensor(np.array([item[0] for item in batch]), dtype=torch.float32)
    reward_target = torch.tensor(np.array([item[2] for item in batch]), dtype=torch.float32)

    # 2. Forward pass
    hidden_state = model.representation(obs_batch)
    prediction_output = model.prediction(hidden_state)
    
    # 3. Extract the tensor from the tuple (assuming structure is (policy, value))
    # If your network returns a tuple, we take the second element (value/reward)
    if isinstance(prediction_output, tuple):
        value_pred = prediction_output[1]
    else:
        value_pred = prediction_output
    
    # 4. Calculate Loss
    loss = F.mse_loss(value_pred.squeeze(), reward_target)

    # 5. Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss
