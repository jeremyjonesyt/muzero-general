BOOTSTRAP_HORIZON_STEPS = 5
import torch
import collections
import random
import numpy as np
try:
    import gymnasium as gym
except ImportError:
    import gym
from self_play import SelfPlayWorker
import torch.optim as optim
import torch.nn as nn

class ReplayBuffer:
    def __init__(self, capacity=50000):
        self.buffer = collections.deque(maxlen=capacity)

    def push(self, trajectory):
        self.buffer.append(trajectory)

    def __len__(self):
        return len(self.buffer)

    def sample_batch(self, batch_size=32, unroll_steps = 10):
        obs_batch, action_batch, policy_batch, value_batch = [], [], [], []
        for _ in range(batch_size):
            traj = random.choice(self.buffer)
            length = len(traj["actions"])
            start_idx = random.randint(0, max(0, length - unroll_steps - 1))
            
            obs = traj["observations"][start_idx]
            actions = traj["actions"][start_idx:start_idx + unroll_steps]
            while len(actions) < unroll_steps:
                actions.append(0)

            policies = traj["search_policies"][start_idx:start_idx + unroll_steps + 1]
            while len(policies) < unroll_steps + 1:
                policies.append(np.array([0.5, 0.5]))

            rewards = traj["rewards"][start_idx:]
            values = [sum(rewards[i:]) for i in range(len(rewards))]
            target_values = values[:unroll_steps + 1]
            while len(target_values) < unroll_steps + 1:
                target_values.append(0.0)

            obs_batch.append(obs)
            action_batch.append(actions)
            policy_batch.append(policies)
            value_batch.append(target_values)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return (
            torch.tensor(np.array(obs_batch), dtype=torch.float32, device=device),
            torch.tensor(np.array(action_batch), dtype=torch.long, device=device),
            torch.tensor(np.array(policy_batch), dtype=torch.float32, device=device),
            torch.tensor(np.array(value_batch), dtype=torch.float32, device=device)
        )

def generate_heuristic_trajectory(env):
    """Generates a high-quality trajectory using an angle-matching heuristic."""
    trajectory = {"observations": [], "actions": [], "search_policies": [], "rewards": []}
    obs, _ = env.reset() if hasattr(env, "reset") and isinstance(env.reset(), tuple) else (env.reset(), {})
    done = False
    truncated = False
    
    while not (done or truncated) and len(trajectory["actions"]) < 500:
        # Heuristic: if pole is leaning right (angle > 0), move right (1). Else move left (0).
        pole_angle = obs[2]
        action = 1 if pole_angle > 0 else 0
        
        trajectory["observations"].append(obs)
        trajectory["actions"].append(action)
        
        # Fake a highly confident search policy target for training guidance
        policy = [0.0, 1.0] if action == 1 else [1.0, 0.0]
        trajectory["search_policies"].append(np.array(policy))
        
        step_results = env.step(action)
        # Unpack, transform raw flat rewards into a continuous quadratic loss penalty, then repack
        next_obs, raw_reward, terminated, truncated, info = step_results
        x, x_dot, theta, theta_dot = next_obs
        # Threshold references for standard CartPole-v1: max_theta ~ 12 deg (0.2095 rad), max_x = 2.4
        shaped_reward = 1.0 - ((theta / 0.2095) ** 2) - ((x / 2.4) ** 2)
        step_results = (next_obs, float(shaped_reward), terminated, truncated, info)
        if len(step_results) == 5:
            obs, reward, done, truncated, _ = step_results
        else:
            obs, reward, done, _ = step_results
            truncated = False
        trajectory["rewards"].append(reward)
        
    return trajectory

def run_master_loop():
    print("[*] Initializing Bootstrapped MuZero Flywheel Optimization Loop...")
    buffer = ReplayBuffer(capacity=50000)
    worker = SelfPlayWorker()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = worker.mcts.model
    optimizer = optim.Adam(model.parameters(), lr=0.00025)
    mse_loss = nn.MSELoss()
    kl_div_loss = nn.KLDivLoss(reduction='batchmean')

    # Seed with 15 heuristic runs to show the network higher value scales
    print("\n[1] Injecting high-horizon heuristic trajectories into buffer...")
    for i in range(15):
        traj = generate_heuristic_trajectory(worker.env)
        buffer.push(traj)
    print(f" -> Successfully seeded {len(buffer)} expert runs. Horizon limit stretched to {len(buffer.buffer[0]['actions'])} steps!")

    # Seed with 15 regular self-play exploration runs
    print("[*] Mixing in 15 exploratory self-play trajectories...")
    for _ in range(15):
        # Inject adaptive root exploration noise dynamically
        worker.mcts.root_dirichlet_alpha = 0.25
        worker.mcts.exploration_fraction = 0.25
        buffer.push(worker.collect_trajectory(num_simulations=30))

    total_iterations = 15
    print(f"\n[2] Launching master training loop with scaled value expectations...")

    for iteration in range(1, total_iterations + 1):
        model.train()
        total_loss = 0.0
        train_steps = 150
        unroll_steps = 10
        batch_size = 32

        for _ in range(train_steps):
            obs, actions, target_policies, target_values = buffer.sample_batch(batch_size=batch_size, unroll_steps=unroll_steps)
            optimizer.zero_grad()

            step_loss = 0.0
            hidden_state, pred_policies, pred_values = model.initial_inference(obs)

            loss_p = kl_div_loss(torch.log(pred_policies + 1e-8), target_policies[:, 0])
            loss_v = mse_loss(pred_values.squeeze(-1), target_values[:, 0])
            step_loss += (loss_p + 0.25 * loss_v)

            for k in range(unroll_steps):
                hidden_state, reward, pred_policies, pred_values = model.recurrent_inference(hidden_state, actions[:, k])
                loss_p = kl_div_loss(torch.log(pred_policies + 1e-8), target_policies[:, k + 1])
                loss_v = mse_loss(pred_values.squeeze(-1), target_values[:, k + 1])
                step_loss += (loss_p + 0.25 * loss_v)

            step_loss /= (unroll_steps + 1)
            step_loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            total_loss += step_loss.item()

        print(f"=== Iteration {iteration:02d}/{total_iterations} | Avg Horizon Loss: {total_loss / train_steps:.4f} ===")
        torch.save(model.state_dict(), "muzero_tripartite_model.pth")

        # Live model evaluation generation
        model.eval()
        new_trajectory = worker.collect_trajectory(num_simulations=30)
        buffer.push(new_trajectory)

    print("\n[+] Optimization production run finished successfully!")

if __name__ == "__main__":
    run_master_loop()















# Automated Scale Injection 
def scale_mcts_value_targets(target_value, gradient_scale=0.25):
    return target_value * gradient_scale

