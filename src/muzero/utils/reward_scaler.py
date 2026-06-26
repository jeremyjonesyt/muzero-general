def normalize_reward(reward, scale_factor=100.0):
    # Scales the reward to prevent gradient explosion
    return reward / scale_factor
