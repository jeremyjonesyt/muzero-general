import math
import torch

class Node:
    def __init__(self, prior):
        self.visit_count = 0
        self.value_sum = 0
        self.prior = prior
        self.children = {}
        self.hidden_state = None
        self.reward = 0

    def expanded(self):
        return len(self.children) > 0

    def value(self):
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

def select_child(node, min_max_stats):
    pb_c_base = 19652
    pb_c_init = 1.25

    exploration_term = math.log((node.visit_count + pb_c_base + 1) / pb_c_base) + pb_c_init
    exploration_term *= math.sqrt(node.visit_count)

    best_score = -float('inf')
    best_action = None
    best_child = None

    for action, child in node.children.items():
        if isinstance(child.prior, torch.Tensor):
            p = child.prior.view(-1)
            idx = int(action) if isinstance(action, (int, float)) else 0
            if idx < len(p):
                prior = p[idx].item()
            else:
                prior = p[0].item()
        else:
            prior = child.prior
            
        val = child.value()
        u_score = exploration_term * prior / (1 + child.visit_count)
        score = float(val + u_score)

        if score > best_score:
            best_score = score
            best_action = action
            best_child = child

    return best_action, best_child
