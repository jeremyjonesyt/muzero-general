import torch
import numpy as np

def get_network(model, target):
    if hasattr(model, target):
        return getattr(model, target)
    raise AttributeError(f"Could not find attribute {target} in model")

def expand_node(node, action, network_output):
    # Ensure Node is imported or defined
    from src.muzero.mcts.node import Node
    node.children[action] = Node(prior=network_output.get('policy_logits', 0.2))

def run_mcts(model, root, num_simulations=10):
    # Simplified simulation loop placeholder
    pass

def get_search_statistics(root, action_space_size):
    """
    Extracts policy and value targets from the MCTS root node.
    """
    visit_counts = np.array([root.children[action].visit_count if action in root.children else 0 
                             for action in range(action_space_size)])
    
    total_visits = np.sum(visit_counts)
    
    # Handle zero-visit case to avoid NaN
    if total_visits == 0:
        policy_target = np.ones(action_space_size) / action_space_size
    else:
        policy_target = visit_counts / total_visits
    
    value_target = root.value()
    
    return {
        'policy_target': torch.tensor(policy_target, dtype=torch.float32),
        'value_target': torch.tensor(value_target, dtype=torch.float32)
    }
