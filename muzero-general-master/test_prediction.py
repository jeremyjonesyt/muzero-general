import requests
import json

# Your engine's endpoint
url = "http://127.0.0.1:8005/muzero_predict"

# Define the game data
game_payload = {
    "away_team": "Reds",
    "home_team": "Phillies",
    "away_fatigue": 0.0,
    "home_fatigue": 0.0,
    "away_pitcher_era": 3.50,
    "home_pitcher_era": 3.20,
    "market_line": -150.0
}

try:
    response = requests.post(url, json=game_payload)
    response.raise_for_status()
    print("--- Prediction Received ---")
    print(json.dumps(response.json(), indent=4))
except Exception as e:
    print(f"Error: {e}")