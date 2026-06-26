import pandas as pd
import os
import smtplib
from email.message import EmailMessage

def send_email(summary_text):
    msg = EmailMessage()
    msg.set_content(f"Training Session Complete. Here is the performance summary:\n\n{summary_text}")
    msg['Subject'] = 'MuZero Training Report'
    msg['From'] = 'muzero.alerts@gmail.com'
    msg['To'] = 'muzero.alerts@gmail.com'
    
    # Using the valid account-specific App Password
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('muzero.alerts@gmail.com', 'oebojtwnatwfcugi')
        server.send_message(msg)
    print("Email sent successfully!")

def generate_report():
    csv_path = r'C:\Users\Dell-Admin\Desktop\MuZero_Projects\muzero_14-0_system\Final_Build\logs_v2\experiment_results.csv'
    if not os.path.exists(csv_path):
        print(f"File not found at: {csv_path}")
        return
    
    df = pd.read_csv(csv_path, names=['Timestamp', 'Episode', 'Loss', 'Reward', 'MCTS_Prob', 'Odds'])
    summary = df[['Loss', 'Reward']].mean().to_string()
    
    print("--- Training Performance Summary ---")
    print(summary)
    send_email(summary)

if __name__ == "__main__":
    generate_report()
