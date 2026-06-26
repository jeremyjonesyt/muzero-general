import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import torch
import torch.nn.functional as F
import csv
from muzero.model.representation import RepresentationNetwork
from muzero.model.dynamics import DynamicsNetwork
from muzero.model.prediction import PredictionNetwork
from muzero.training.replay_buffer import ReplayBuffer
from muzero.training.inference_loop import MuZeroModelWrapper

LOG_FILE = 'loss_log.csv'

def train_step(model, replay_buffer, optimizer, batch_size=1):
    state, action, target_policy, target_value = replay_buffer.sample(batch_size)
    hidden, policy_logits, value = model.initial_inference(state)
    
    # FIX: Squeeze the logits to [1, 5] if they are [1, 1, 5]
    if policy_logits.dim() == 3:
        policy_logits = policy_logits.squeeze(1)
        
    log_probs = F.log_softmax(policy_logits, dim=-1)
    target = torch.tensor([2], dtype=torch.long)
    
    loss = F.mse_loss(value.view(-1), target_value.view(-1)) + F.nll_loss(log_probs, target)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([loss.item()])
    return loss.item()

if __name__ == '__main__':
    model = MuZeroModelWrapper(RepresentationNetwork(), DynamicsNetwork(), PredictionNetwork())
    buffer = ReplayBuffer()
    optimizer = torch.optim.Adam(model.parameters())
    
    buffer.push(torch.randn(1, 5), torch.tensor([1]), torch.tensor([0, 0, 1, 0, 0]), torch.tensor([0.5]))
    
    loss = train_step(model, buffer, optimizer)
    print(f"Test training step complete. Loss: {loss}")
