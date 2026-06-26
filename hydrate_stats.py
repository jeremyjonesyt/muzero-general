import statsapi
import json
import os
from datetime import datetime

base_data_dir = r'C:\Users\Dell-Admin\Desktop\muzero_14-0_system\data'
today_str = datetime.now().strftime('%Y-%m-%d')
daily_data_dir = os.path.join(base_data_dir, today_str)

if not os.path.exists(daily_data_dir):
    os.makedirs(daily_data_dir)

def hydrate_todays_data():
    try:
        schedule = statsapi.schedule(date=today_str)
        print(f'Fetching {len(schedule)} games for {today_str}...')
        
        for game in schedule:
            # Use 'game_id' instead of 'game_pk' as confirmed by debug output
            game_id = game.get('game_id')
            if not game_id:
                continue
                
            try:
                boxscore = statsapi.boxscore(game_id)
                filename = os.path.join(daily_data_dir, f'game_{game_id}.json')
                with open(filename, 'w') as f:
                    json.dump(boxscore, f)
                print(f'Hydrated game {game_id}')
            except Exception as e:
                print(f'Failed to hydrate game {game_id}: {e}')
    except Exception as e:
        print(f'Critical error fetching schedule: {e}')

if __name__ == '__main__':
    hydrate_todays_data()
