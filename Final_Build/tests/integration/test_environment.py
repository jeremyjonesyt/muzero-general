from muzero.env.environment import MLBEnvironment
from muzero.data.loader import MLBDataLoader

def test_environment_step():
    loader = MLBDataLoader()
    env = MLBEnvironment(loader)
    env.reset(108)
    next_state, reward, done = env.step(action=1)
    
    assert reward == 1.0
    assert len(next_state) == 10
