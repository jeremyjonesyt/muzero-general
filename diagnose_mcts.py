import torch
import numpy as np
from self_play import SelfPlayWorker

def inspect_first_step():
    worker = SelfPlayWorker()
    worker.mcts.model.eval()
    
    obs, _ = worker.env.reset() if hasattr(worker.env, "reset") and isinstance(worker.env.reset(), tuple) else (worker.env.reset(), {})
    
    print("\n====================================================")
    print("        MUZERO MCTS ROOT-LEVEL DIAGNOSTICS          ")
    print("====================================================")
    
    # Run initial inference directly
    with torch.no_grad():
        hidden, policy, value = worker.mcts.model.initial_inference(
            torch.tensor(np.array([obs]), dtype=torch.float32)
        )
    
    print(f"[*] Raw Model Observation Input: {obs}")
    print(f"[+] Raw Policy Network Prior Output: {policy.numpy()[0]}")
    print(f"[+] Raw Value Network Prediction:     {value.item():.4f}")
    
    # Now run MCTS search and see what happens to the visit counts
    root = worker.mcts.run_search(obs, num_simulations=50)
    
    print("\n--- MCTS Tree Expansion Results (50 Simulations) ---")
    for a in range(worker.action_dim):
        child = root.children[a]
        print(f" -> Action {a}: Visits = {child.visit_count:2d} | Prior = {child.prior:.4f} | Q-Value = {child.value():.4f}")
    
    print("====================================================")

if __name__ == "__main__":
    inspect_first_step()
