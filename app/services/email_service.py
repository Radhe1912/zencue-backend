import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

import smtplib
import socket
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(to_email, message):
    msg = MIMEText(message)
    msg["Subject"] = "ZenCue Reminder"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    # ✅ Force IPv4
    socket.setdefaulttimeout(10)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.connect("smtp.gmail.com", 465)  # forces fresh connection
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent")

    except Exception as e:
        print("❌ Email error:", e)