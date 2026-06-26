import torch
import torch.nn.functional as F

def calculate_loss(network_output, targets):
    """
    Calculates the combined multi-task loss for MuZero.
    network_output: dict containing 'policy_logits', 'value', 'reward'
    targets: dict containing 'policy_target', 'value_target', 'reward_target'
    """
    # 1. Policy Loss (Cross-Entropy)
    policy_loss = F.cross_entropy(network_output['policy_logits'], targets['policy_target'])
    
    # 2. Value Loss (MSE)
    value_loss = F.mse_loss(network_output['value'], targets['value_target'])
    
    # 3. Reward Loss (MSE)
    reward_loss = F.mse_loss(network_output['reward'], targets['reward_target'])
    
    # Combine losses
    total_loss = policy_loss + value_loss + reward_loss
    
    return total_loss
