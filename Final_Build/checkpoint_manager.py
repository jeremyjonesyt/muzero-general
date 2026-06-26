import shutil
import os
import pandas as pd

def save_checkpoint(episode, reward):
    archive_dir = 'Models_Archive'
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    
    # Define source and destination
    source = 'src/muzero/model/weights.pth'
    dest = f'{archive_dir}/model_ep{episode}_reward{reward:.2f}.pth'
    
    if os.path.exists(source):
        shutil.copy(source, dest)
        print(f"Checkpoint saved: {dest}")

if __name__ == '__main__':
    # Logic to trigger after report
    df = pd.read_csv('logs/experiment_results.csv')
    best = df.loc[df['reward'].idxmax()]
    save_checkpoint(best['episode'], best['reward'])
