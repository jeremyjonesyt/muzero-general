import torch
import torch.nn.functional as F

def calculate_step_loss(policy_pred, value_pred, reward_pred, targets):
    # targets: (policy_target, value_target, reward_target)
    policy_target, value_target, reward_target = targets
    
    # Standard MuZero Loss Components:
    # 1. Policy Loss (Cross Entropy)
    policy_loss = F.cross_entropy(policy_pred, policy_target)
    
    # 2. Value Loss (MSE or L1)
    value_loss = F.mse_loss(value_pred, value_target)
    
    # 3. Reward Loss (MSE)
    reward_loss = F.mse_loss(reward_pred, reward_target)
    
    return policy_loss + value_loss + reward_loss
