from muzero.agent import MuZeroAgent

def test_agent_initialization():
    agent = MuZeroAgent()
    assert agent.name == 'MuZero_14_0'
