import sys
import os
sys.path.append(r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system')

import schedule
import time
import pandas as pd
from datetime import datetime, timedelta

# Updated import path to match: src -> muzero -> training
from src.muzero.training.inference_engine import InferenceEngine
from src.muzero.training.email_utils import send_picks_email

engine = InferenceEngine('best_model.pth', {"learning_rate": 1e-4})
schedule_file = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\data\daily_schedule.csv'

def process_game_window():
    if not os.path.exists(schedule_file): return
    df = pd.read_csv(schedule_file)
    now = datetime.now()
    
    for _, game in df.iterrows():
        game_time = pd.to_datetime(game['start_time'])
        if game_time - timedelta(hours=1) <= now < game_time - timedelta(minutes=55):
            print(f"Triggering inference for: {game['matchup']}")
            engine.run_inference(game['data_path'], 'temp_picks.csv')
            send_picks_email('temp_picks.csv')

schedule.every(15).minutes.do(process_game_window)
print('Monitor active. Polling schedule every 15 minutes.')

while True:
    schedule.run_pending()
    time.sleep(60)
