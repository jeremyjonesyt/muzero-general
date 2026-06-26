import os
import time
import json
import random

QUEUE_DIR = "data/queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

def parse_game_to_tensor():
    """Maps live plays to features expected by MuZero."""
    # (Your logic here - simplified for demonstration)
    features = [float(random.randint(1, 9)), float(random.randint(0, 2)), 0.0, 0.0]
    return features

if __name__ == "__main__":
    print("Ingestion engine active...")
    while True:
        # Ingestion logic
        time.sleep(1)
