import torch
from src.muzero.data.mapper import map_game_state_to_tensor

class MuZeroEnvWrapper:
    def __init__(self, game):
        self.game = game

    def reset(self):
        # Retrieve the raw state from the environment
        raw_state = self.game.reset(team_id='1')
        
        # Translate the dictionary state into the tensor format the model expects
        # Ensure raw_state is in the dictionary format: {'player_x': ..., 'player_y': ..., ...}
        return map_game_state_to_tensor(raw_state)

    def step(self, action):
        # Get raw data and reward from the game engine
        raw_next_state, reward, done = self.game.step(action)
        
        # Map the next state to a tensor
        state_tensor = map_game_state_to_tensor(raw_next_state)
        
        return state_tensor, reward, done
