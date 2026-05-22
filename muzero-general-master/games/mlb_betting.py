import os
import torch

class MuZeroConfig:
    def __init__(self):
        self.seed = 42
        self.observation_shape = (1, 1, 5) 
        self.action_space = list(range(2))  # 0: Away, 1: Home
        self.players = [0]
        self.stacked_observations = 0
        self.muzero_player = 0
        self.opponent = None
        self.num_workers = 1
        self.selfplay_on_gpu = torch.cuda.is_available()
        self.max_moves = 1
        self.num_simulations = 30
        self.discount = 0.997
        self.root_dirichlet_alpha = 0.25
        self.root_exploration_fraction = 0.25
        self.pb_c_base = 19652
        self.pb_c_init = 1.25
        self.network = "fullyconnected"
        self.blocks = 2
        self.channels = 16
        self.reduced_channels_reward = 16
        self.reduced_channels_value = 16
        self.reduced_channels_policy = 16
        
        # 🧠 Fully Connected Architecture Layers
        self.fc_representation_layers = [16]
        self.fc_dynamics_layers = [16]
        self.fc_reward_layers = [16]
        self.fc_value_layers = [16]
        self.fc_policy_layers = [16]
        
        self.support_size = 10
        self.encoding_size = 10
        self.value_support_size = 10
        self.reward_support_size = 10

    def visit_softmax_temperature_fn(self, trained_steps):
        return 1.0