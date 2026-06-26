import torch

def map_game_state_to_tensor(raw_state):
    # Normalize inputs: scale raw values to range [-1, 1] or [0, 1]
    player_x = raw_state['player_x'] / 100.0
    player_y = raw_state['player_y'] / 100.0
    velocity = raw_state['velocity'] / 10.0 
    distance = raw_state['distance_to_goal'] / 500.0
    
    state_values = [player_x, player_y, velocity, distance]
    return torch.tensor(state_values, dtype=torch.float32).unsqueeze(0)
