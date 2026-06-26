import os
import sys
import json
import time
import requests

def fetch_and_save():
    queue_dir = "data/queue"
    if not os.path.exists(queue_dir):
        os.makedirs(queue_dir)
        
    # Official MLB Live Scoreboard / Play-by-Play endpoint
    # Pulls all games scheduled for today's date dynamically
    date_str = time.strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=linescore,plays"
    
    print(f"Connecting to MLB API for date: {date_str}...")
    try:
        # ?? CRITICAL: Explicit short timeouts prevent infinite process stalls
        response = requests.get(url, timeout=(5, 10))
        response.raise_for_status()
        data = response.json()
        
        # Check if games exist for today
        dates = data.get("dates", [])
        if not dates or not dates[0].get("games"):
            print("No live games found scheduled for today. Generating simulated fallback tensor...")
            # Simulated game event tensor structure to keep MuZero optimization warm
            sample_payload = {
                "game_id": 999999,
                "timestamp": time.time(),
                "inning": 5,
                "outs": 1,
                "balls": 2,
                "strikes": 1,
                "home_score": 3,
                "away_score": 2,
                "state_tensor": [0.5, 0.2, 0.1, 0.9, 0.0, 1.0, 0.3]
            }
            file_path = os.path.join(queue_dir, f"sample_{int(time.time() * 1000)}.json")
            with open(file_path, "w") as f:
                json.dump(sample_payload, f)
            print(f"Saved warm-start data frame: {file_path}")
            return

        # Loop over active games and extract features
        games = dates[0]["games"]
        for game in games:
            game_id = game.get("gamePk")
            linescore = game.get("linescore", {})
            
            # Extract live features
            current_inning = linescore.get("currentInning", 1)
            is_top = linescore.get("isTopInning", True)
            outs = linescore.get("outs", 0)
            
            # Compile features into structural sample tracking states
            sample_payload = {
                "game_id": game_id,
                "timestamp": time.time(),
                "inning": current_inning,
                "is_top_inning": 1 if is_top else 0,
                "outs": outs,
                "home_score": linescore.get("teams", {}).get("home", {}).get("runs", 0),
                "away_score": linescore.get("teams", {}).get("away", {}).get("runs", 0)
            }
            
            file_path = os.path.join(queue_dir, f"sample_{game_id}_{int(time.time() * 1000)}.json")
            with open(file_path, "w") as f:
                json.dump(sample_payload, f)
            print(f"Successfully processed and serialized live data block: {file_path}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] MLB API Connection Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    fetch_and_save()
