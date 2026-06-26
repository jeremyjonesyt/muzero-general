import smtplib
from email.message import EmailMessage

def test_connection():
    try:
        msg = EmailMessage()
        msg.set_content("This is a connection test from your MuZero automated system.")
        msg['Subject'] = 'MuZero System Test'
        msg['From'] = 'muzero.alerts@gmail.com'
        msg['To'] = 'muzero.alerts@gmail.com'

        # REPLACE WITH YOUR ACTUAL 16-CHARACTER APP PASSWORD
        app_password = 'PASTE_YOUR_16_CHAR_APP_PASSWORD_HERE' 
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('muzero.alerts@gmail.com', app_password)
            server.send_message(msg)
        print("Test email sent successfully to muzero.alerts@gmail.com")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    test_connection()
