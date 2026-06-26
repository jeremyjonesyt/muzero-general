import numpy as np

class MLBEnvironment:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.current_state = None

    def reset(self, team_id):
        # Return the dictionary format that map_game_state_to_tensor expects
        return {
            'player_x': 0.1, 
            'player_y': 0.2, 
            'velocity': 0.3, 
            'distance_to_goal': 0.4
        }

    def step(self, action):
        reward = 1.0 if action == 1 else 0.0
        # Return the next state as a dictionary
        next_state = {
            'player_x': np.random.rand(), 
            'player_y': np.random.rand(), 
            'velocity': np.random.rand(), 
            'distance_to_goal': np.random.rand()
        }
        done = False
        return next_state, reward, done
