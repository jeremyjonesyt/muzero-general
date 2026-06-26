import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

import torch
import gymnasium as gym
import random
from muzero.model.networks import RepresentationNetwork, PredictionNetwork
from muzero.training.replay_buffer import ReplayBuffer
from muzero.training.bptt import run_bptt
from muzero.env_interface import play_game
from muzero.mcts import MCTS

class MuZeroModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.representation = RepresentationNetwork(4, 64)
        self.prediction = PredictionNetwork(64, 2)

if __name__ == '__main__':
    model = MuZeroModel()
    buffer = ReplayBuffer(buffer_size=5000)
    mcts = MCTS(model)
    env = gym.make('CartPole-v1')

    print('Starting improved exploration training...')
    epsilon = 0.5
    
    try:
        iteration = 0
        while True:
            iteration += 1
            game_history = []
            
            # Epsilon-Greedy: Roll out a mini-episode to gather diverse data
            if random.random() < epsilon:
                obs, _ = env.reset()
                for _ in range(20): # Explore up to 20 steps
                    action = env.action_space.sample()
                    next_obs, reward, done, truncated, _ = env.step(action)
                    game_history.append((obs, action, reward))
                    obs = next_obs
                    if done or truncated: break
            else:
                game_history = play_game(model, env, mcts)
            
            buffer.save_game(game_history)
            if epsilon > 0.1: epsilon *= 0.999
            
            total_reward = sum(step[2] for step in game_history)
            batch = buffer.sample_batch(batch_size=32)
            if batch:
                loss = run_bptt(model, batch)
                print(f'Iteration {iteration} | Epsilon: {epsilon:.3f} | Reward: {total_reward} | Loss: {loss.item():.4f}')
    except KeyboardInterrupt:
        buffer.save_to_disk()
        print('Training stopped. Progress saved.')
