from train_enhanced import Trainer
from buffer import ReplayBuffer
from src.muzero.env.environment import MLBEnvironment
from src.muzero.env.wrapper import MuZeroEnvWrapper
from src.muzero.data.loader import MuZeroDataLoader
# Assuming you have your model class defined here or imported
import torch

# Initialize
model = MuZeroModel() # Ensure this is the same class as in evaluate.py
trainer = Trainer(model)
buffer = ReplayBuffer()
env = MuZeroEnvWrapper(MLBEnvironment(MuZeroDataLoader(model=model)))

# Simple Training Loop
for episode in range(100):
    state = env.reset()
    total_loss = 0
    for step in range(15):
        action = trainer.get_action(state, 5)
        next_state, reward, done = env.step(action)
        buffer.push(state, action, reward, next_state)
        
        # Train if we have enough data
        if len(buffer.buffer) > 32:
            states, actions, rewards, next_states = buffer.sample(32)
            # In a real MuZero, you'd use MCTS here; 
            # for now, we use a mock target
            target_policy = torch.zeros(32, 5)
            target_policy[range(32), actions] = 1.0
            total_loss = trainer.train_step((states, target_policy, rewards.unsqueeze(1)))
            
        state = next_state
        if done: break
    
    trainer.update_epsilon()
    if episode % 10 == 0:
        print(f'Episode {episode} | Epsilon: {trainer.epsilon:.2f} | Last Loss: {total_loss:.4f}')

