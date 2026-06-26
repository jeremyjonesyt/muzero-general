import statsapi
import json
from datetime import datetime

def debug_schedule():
    today_str = datetime.now().strftime('%Y-%m-%d')
    schedule = statsapi.schedule(date=today_str)
    
    if schedule:
        print(f"Found {len(schedule)} items.")
        print("Structure of the first item:")
        print(json.dumps(schedule[0], indent=2))
    else:
        print("No games found in schedule.")

if __name__ == '__main__':
    debug_schedule()
