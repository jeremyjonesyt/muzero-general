import json
import os

def load_config(config_path=r"C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\config.json"):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Config file not found at {config_path}")
