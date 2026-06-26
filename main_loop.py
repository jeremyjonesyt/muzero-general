from src.muzero.training.replay_buffer import ReplayBuffer

buffer = ReplayBuffer(buffer_size=100)

# After Self-Play:
# game_history = [(obs, action, policy, value, reward), ...]
# buffer.save_game(game_history)

# During Training:
# batch = buffer.sample_batch()
# train_step(batch, input_data)
