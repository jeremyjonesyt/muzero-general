import torch
import numpy as np
try:
    import gymnasium as gym
except ImportError:
    import gym
from mcts import MuZeroMCTS

class SelfPlayWorker:
    def __init__(self):
        self.action_dim = 2
        self.env = gym.make("CartPole-v1")
        self.mcts = MuZeroMCTS(action_dim=self.action_dim)

        try:
            self.mcts.model.load_state_dict(torch.load("muzero_tripartite_model.pth"))
            print("[+] Loaded trained tripartite weights for self-play.")
        except Exception:
            print("[*] Running self-play with fresh initialized network weights.")

    def collect_trajectory(self, num_simulations=30, temperature=1.0):
        trajectory = {
            "observations": [],
            "actions": [],
            "search_policies": [],
            "rewards": []
        }

        obs, _ = self.env.reset() if hasattr(self.env, "reset") and isinstance(self.env.reset(), tuple) else (self.env.reset(), {})
        done = False
        truncated = False
        step_count = 0

        while not (done or truncated) and step_count < 200:
            root = self.mcts.run_search(obs, num_simulations=num_simulations)

            visit_counts = np.array([root.children[a].visit_count for a in range(self.action_dim)])
            sum_visits = np.sum(visit_counts)
            
            if sum_visits == 0:
                policy_target = np.ones(self.action_dim) / self.action_dim
            else:
                policy_target = visit_counts / sum_visits

            # EXPLORATION FIX: Instead of hard argmax, sample from the distribution!
            if temperature == 0:
                action = int(np.argmax(policy_target))
            else:
                # Apply temperature scaling to the probabilities
                scaled_probs = np.power(policy_target, 1.0 / temperature)
                scaled_probs /= np.sum(scaled_probs)
                action = int(np.random.choice(self.action_dim, p=scaled_probs))

            trajectory["observations"].append(obs)
            trajectory["actions"].append(action)
            trajectory["search_policies"].append(policy_target)

            step_results = self.env.step(action)
            if len(step_results) == 5:
                next_obs, reward, done, truncated, _ = step_results
            else:
                next_obs, reward, done, _ = step_results
                truncated = False

            trajectory["rewards"].append(reward)
            obs = next_obs
            step_count += 1

        return trajectory

if __name__ == "__main__":
    worker = SelfPlayWorker()
    traj = worker.collect_trajectory(num_simulations=20, temperature=1.0)
    print(f"[+] Sample Actions Chosen: {traj['actions']}")
