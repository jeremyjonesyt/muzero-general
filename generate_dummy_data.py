import json
import os
import random
import time

def generate():
    os.makedirs('data/queue', exist_ok=True)
    while True:
        reward = random.uniform(-1, 1)
        # Create a deterministic pattern: 
        # Action 0 for negative, 1 for positive, 2 for near zero
        if reward > 0.3: action = 1
        elif reward < -0.3: action = 0
        else: action = 2
        
        data = {'action': action, 'reward': reward, 'value': reward**2}
        filename = f"data/queue/sample_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(data, f)
        time.sleep(0.5)

if __name__ == '__main__':
    generate()
