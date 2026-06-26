import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_discord_alert(message):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print('Error: DISCORD_WEBHOOK_URL not found in .env')
        return
        
    payload = {'content': f'?? **MuZero Update:** {message}'}
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f'Failed to send alert: {e}')
