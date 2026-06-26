import pandas as pd
import yaml

def generate_report():
    df = pd.read_csv('logs/experiment_results.csv')
    best_episode = df.loc[df['reward'].idxmax()]
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print("--- Experiment Performance Summary ---")
    print(f"Best Reward: {best_episode['reward']} at Episode {best_episode['episode']}")
    print(f"Current Config: {config}")
    print("---------------------------------------")

if __name__ == '__main__':
    generate_report()
