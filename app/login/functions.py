from flask_mail import Mail, Message
from app import main, email_config

def send_mail(recipients : list, message : dict):
    mail = Mail(main)
    msg = Message(body=message['message'], subject=message['subject'], sender=email_config['username'], recipients=recipients)
    mail.send(msg)

def verify_email(email):
    email = email.strip()
    
def verify_password(password):
    if len(password) > 7:
        return True
    return False