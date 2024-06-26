from smtplib import SMTP
from email.message import EmailMessage
import os


class EnvException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else "Something went wrong"

    def __str__(self):
        return f"\033[91mEnvironment exception: {self.message}\033[0m"


def send_email(message, recipient):
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    try:
        if not email or not password:
            raise EnvException("variables EMAIL_ADDRESS and EMAIL_PASSWORD are not set")
    except EnvException as e:
        print(e)
        print("Email did not send")
    else:
        msg = EmailMessage()
        msg["Subject"] = "Task Manager registration"
        msg["From"] = email
        msg["To"] = recipient
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(message)

        s = SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(email, password)
        s.send_message(msg)
        s.quit()
