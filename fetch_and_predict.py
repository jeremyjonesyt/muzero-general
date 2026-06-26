import smtplib
import os
from email.message import EmailMessage

def send_picks_email(predictions_summary):
    sender_email = "muzero.alerts@gmail.com" 
    receiver_email = "muzero.alerts@gmail.com"
    # Ensure your system environment variable 'EMAIL_PASSWORD' is set
    password = "qgjcjyyscmxwvejd" 

    msg = EmailMessage()
    msg['Subject'] = "Daily MLB Predictions - Automated System"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(f"Here are your daily picks:\n\n{predictions_summary}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    # Your prediction logic goes here
    summary = "Example Prediction: Phillies win vs Marlins"
    send_picks_email(summary)
