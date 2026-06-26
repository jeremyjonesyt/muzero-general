import torch
import math
import numpy as np
from models import CompleteMuZeroNet

class Node:
    def __init__(self, prior):
        self.prior = prior
        self.visit_count = 0
        self.value_sum = 0.0
        self.children = {}
        self.hidden_state = None
        self.reward = 0.0

    def value(self):
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

class MuZeroMCTS:
    def __init__(self, action_dim=2):
        self.action_dim = action_dim
        self.model = CompleteMuZeroNet(input_dim=4, action_dim=action_dim, hidden_dim=64)
        self.model.eval()
        self.c1 = 1.25  
        self.discount = 0.99 

    def run_search(self, raw_observation, num_simulations=30):
        device = next(self.model.parameters()).device
        obs_tensor = torch.tensor(np.array([raw_observation]), dtype=torch.float32, device=device)

        with torch.no_grad():
            hidden_state, policy_logits, value = self.model.initial_inference(obs_tensor)

        root = Node(prior=1.0)
        root.hidden_state = hidden_state[0]
        
        # Populate initial root priors
        priors = policy_logits[0].cpu().numpy()
        alpha = 0.3
        epsilon = 0.25
        noise = np.random.dirichlet([alpha] * self.action_dim)

        for a in range(self.action_dim):
            mixed_prior = (1 - epsilon) * priors[a] + epsilon * noise[a]
            root.children[a] = Node(prior=mixed_prior)

        for _ in range(num_simulations):
            node = root
            search_path = [node]
            actions_taken = []

            # 1. Select down the tree using PUCT until we hit a node that hasn't been expanded yet
            while len(node.children) > 0:
                total_visits = sum(child.visit_count for child in node.children.values())
                best_action = None
                best_score = -float('inf')

                for a, child in node.children.items():
                    u = child.prior * (math.sqrt(total_visits + 1) / (1 + child.visit_count)) * self.c1
                    score = child.reward + child.value() + u
                    if score > best_score:
                        best_score = score
                        best_action = a

                actions_taken.append(best_action)
                node = node.children[best_action]
                search_path.append(node)
                
                # If this child hasn't received a hidden state yet, it's our leaf node to expand!
                if node.hidden_state is None:
                    break

            # 2. Expand the leaf node if it's new
            if node.hidden_state is None and len(actions_taken) > 0:
                parent_node = search_path[-2]
                chosen_action = actions_taken[-1]
                act_tensor = torch.tensor([chosen_action], dtype=torch.long, device=device)
                hid_tensor = parent_node.hidden_state.unsqueeze(0)

                with torch.no_grad():
                    next_hidden, reward, policy_logits, value_pred = self.model.recurrent_inference(hid_tensor, act_tensor)

                node.hidden_state = next_hidden[0]
                node.reward = reward.item()
                v_estimate = value_pred.item()

                leaf_priors = policy_logits[0].cpu().numpy()
                for a in range(self.action_dim):
                    node.children[a] = Node(prior=leaf_priors[a])
            else:
                v_estimate = value.item()

            # 3. Backpropagate
            for i in range(len(search_path) - 1, -1, -1):
                path_node = search_path[i]
                path_node.visit_count += 1
                path_node.value_sum += v_estimate
                if i > 0:
                    v_estimate = search_path[i].reward + self.discount * v_estimate

        return root
