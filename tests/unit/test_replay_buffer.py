from muzero.data.replay_buffer import ReplayBuffer

def test_replay_buffer_operations():
    buffer = ReplayBuffer(capacity=10)
    
    # Simulate saving a game
    buffer.save_game({'observation': [0, 1], 'action': 1})
    assert len(buffer) == 1
    
    # Simulate sampling
    batch = buffer.sample_batch(1)
    assert len(batch) == 1
    assert batch[0]['action'] == 1
