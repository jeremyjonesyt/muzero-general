import torch
import numpy as np
import random

def play_game(model, env, mcts, stochastic=True):
    history = []
    obs, _ = env.reset(seed=random.randint(0, 10000) if stochastic else 42)
    done = False
    truncated = False
    while not (done or truncated):
        obs_tensor = torch.tensor(np.array(obs), dtype=torch.float32).unsqueeze(0)
        state = model.representation(obs_tensor)
        action = mcts.run(state)
        history.append((obs, action, 0))
        obs, reward, done, truncated, _ = env.step(action)
    return history
