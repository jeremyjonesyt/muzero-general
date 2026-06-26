import pandas as pd
import requests
import json
import os

WEBHOOK_URL = 'PASTE_YOUR_WEBHOOK_URL_HERE'

def send_to_discord(csv_file):
    if not os.path.exists(csv_file):
        print(f'Error: {csv_file} not found.')
        return
    df = pd.read_csv(csv_file)
    report = f'### 📊 Daily Matchup Report: 14-0 System\n\\\\n{df.to_string()}\n\\\'
    payload = {'content': report}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print('Report successfully delivered to Discord.')
    else:
        print(f'Failed to send. Status Code: {response.status_code}')

if __name__ == '__main__':
    send_to_discord('season_2026_predictions.csv')
