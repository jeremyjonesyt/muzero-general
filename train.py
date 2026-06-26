import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from models import CompleteMuZeroNet

def load_unrolled_batch(batch_size=32, unroll_steps = 10, action_dim=2):
    """
    Simulates a sequence batch from the replay buffer synchronized to CartPole dimensions.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    obs = torch.randn(batch_size, 4, device=device)
    # Actions are strictly restricted to 0 or 1
    actions = torch.randint(0, action_dim, (batch_size, unroll_steps), device=device)
    target_policies = torch.randint(0, action_dim, (batch_size, unroll_steps + 1), device=device)
    target_values = torch.randn(batch_size, unroll_steps + 1, device=device)
    return obs, actions, target_policies, target_values

def train_unrolled():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    action_dim = 2  # Match CartPole action space dimensions exactly
    unroll_steps = 10
    batch_size = 32

    print(f"[*] Training script connecting tripartite model on {device} (Action Dim: {action_dim})...")
    
    # Initialize network with 2 action outputs
    model = CompleteMuZeroNet(input_dim=4, action_dim=action_dim, hidden_dim=256).to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    mse_loss = nn.MSELoss()
    kl_div_loss = nn.KLDivLoss(reduction='batchmean')

    print("[*] Starting multi-step recurrent sequence training loop...")
    for step in range(301):
        obs, actions, target_policies, target_values = load_unrolled_batch(batch_size, unroll_steps, action_dim)
        optimizer.zero_grad()
        
        total_loss = 0.0
        
        # --- Step 0: Initial Inference (Representation -> Prediction) ---
        hidden_state, pred_policies, pred_values = model.initial_inference(obs)
        
        # Match one-hot targets to the 2-action dimension output space
        target_policy_0 = F.one_hot(target_policies[:, 0].long(), num_classes=action_dim).float()
        loss_p = kl_div_loss(torch.log(pred_policies + 1e-8), target_policy_0)
        loss_v = mse_loss(pred_values.squeeze(-1), target_values[:, 0])
        total_loss += (loss_p + loss_v)
        
        # --- Steps 1 to K: Recurrent Unrolling (Dynamics -> Prediction) ---
        for k in range(unroll_steps):
            action_k = actions[:, k]
            hidden_state, reward, pred_policies, pred_values = model.recurrent_inference(hidden_state, action_k)
            
            target_policy_k = F.one_hot(target_policies[:, k + 1].long(), num_classes=action_dim).float()
            loss_p = kl_div_loss(torch.log(pred_policies + 1e-8), target_policy_k)
            loss_v = mse_loss(pred_values.squeeze(-1), target_values[:, k + 1])
            
            total_loss += (loss_p + loss_v)
            
        # Normalize loss over full sequence horizon depth
        total_loss /= (unroll_steps + 1)
        
        total_loss.backward()
        optimizer.step()
        
        if step % 50 == 0:
            print(f"Batch Step {step:3d} | Unrolled Mean Horizon Loss: {total_loss.item():.6f}")

    torch.save(model.state_dict(), "muzero_tripartite_model.pth")
    print("[+] Tripartite training complete. 2-Action Weights saved to muzero_tripartite_model.pth")

if __name__ == "__main__":
    train_unrolled()


