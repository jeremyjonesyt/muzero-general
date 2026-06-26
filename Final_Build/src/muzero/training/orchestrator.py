from torch.utils.tensorboard import SummaryWriter  # Added Import
from muzero.config_loader import load_config
from muzero.data.loader import MLBDataLoader
from muzero.mcts.mcts import MCTS, Node
from muzero.training.trainer import MuZeroTrainer
from muzero.env.environment import MLBEnvironment
import csv
import datetime

class TrainingOrchestrator:
    def __init__(self):
        self.writer = SummaryWriter('logs_v2') # Initialized Writer
        self.current_step = 0                  # Added Step Counter
        self.config = load_config()
        self.data_loader = MLBDataLoader()
        self.env = MLBEnvironment(self.data_loader)
        self.mcts = MCTS(config=self.config)
        self.trainer = MuZeroTrainer(config=self.config)
        self.episode = 0
        
    def log_result(self, loss, reward):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs/experiment_results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, self.episode, loss, reward])
        
        # Add TensorBoard Logging
        self.writer.add_scalar('Loss', loss, self.current_step)
        self.writer.add_scalar('Reward', reward, self.current_step)
        self.current_step += 1

    def run_full_episode(self, team_id):
        self.episode += 1
        state = self.env.reset(team_id)
        
        root = Node(prior=1.0)
        self.mcts.run_mcts(root, None)
        action = 1 
        next_state, reward, done = self.env.step(action)
        
        loss = self.trainer.train_step(next_state)
        
        self.log_result(loss, reward)
        return loss, reward