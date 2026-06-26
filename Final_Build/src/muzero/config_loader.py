import yaml
import os

def load_config(config_path='config.yaml'):
    if not os.path.exists(config_path):
        return {
            'learning_rate': 0.001,
            'mcts_simulations': 50,
            'discount_factor': 0.99,
            'batch_size': 32
        }
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
