import torch
import os
import json
import glob

class MuZeroDataLoader:
    def __init__(self, model=None, batch_size=1):
        self.batch_size = batch_size
        self.queue_dir = "data/queue"
        
    def sample_batch(self):
        files = glob.glob(os.path.join(self.queue_dir, "sample_*.json"))
        
        # Match model's input feature size expectation precisely (4 features)
        default_feature_count = 4
        
        if not files:
            features = [0.0] * default_feature_count
            target_action = 2
            target_value = 0.0
            target_reward = 0.0
        else:
            target_file = min(files, key=os.path.getctime)
            try:
                with open(target_file, 'r') as f:
                    data = json.load(f)
                
                # If parsing files, ensure we isolate exactly the first 4 features to prevent crashes
                features = data['features'][:default_feature_count]
                target_action = data['action']
                target_value = data['value']
                target_reward = data['reward']
                os.remove(target_file)
            except Exception:
                features = [0.0] * default_feature_count
                target_action = 2
                target_value = 0.0
                target_reward = 0.0

        input_data = torch.tensor([features], dtype=torch.float32)
        
        policy_target = torch.tensor([target_action], dtype=torch.long)
        value_target = torch.tensor([[target_value]], dtype=torch.float32)
        reward_target = torch.tensor([[target_reward]], dtype=torch.float32)
        
        return input_data, (policy_target, value_target, reward_target)
