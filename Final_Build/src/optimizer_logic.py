# Add this snippet to your run_session.py logic
def get_lr(episode):
    # Decay learning rate every 500 episodes
    return base_lr * (0.95 ** (episode // 500))
