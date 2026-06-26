import statsapi
import json
import os

data_dir = r"C:\Users\Dell-Admin\Desktop\muzero_14-0_system\data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def fetch_todays_data():
    try:
        schedule = statsapi.schedule(date="06/16/2026")
        output_path = os.path.join(data_dir, "todays_games.json")
        with open(output_path, "w") as f:
            json.dump(schedule, f)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_todays_data()
