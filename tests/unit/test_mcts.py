from muzero.mcts.mcts import Node, MCTS

def test_ucb_calculation():
    mcts = MCTS({})
    parent = Node(prior=1.0)
    parent.visit_count = 10
    child = Node(prior=0.5)
    child.visit_count = 2
    child.value_sum = 1.0
    
    score = mcts.ucb_score(parent, child)
    assert score > 0

def test_mcts_run():
    mcts = MCTS({})
    root = Node(prior=1.0)
    root.children[0] = Node(prior=0.5)
    result = mcts.run_mcts(root, None)
    assert result == "MCTS simulation complete with UCB"
