import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
RESTOCK_EMAIL_LIST = os.environ.get("RESTOCK_EMAIL_LIST")


def send_multiple_emails(smtp, email_list):
    for email in email_list:
        send_email(smtp, email)


def send_email(smtp, email):
    email_message = create_email_message(email)
    smtp.send_message(email_message)


def create_email_message(recipient_email):
    message = EmailMessage()
    message["Subject"] = "Hello World!"
    message["From"] = SMTP_USER
    message["To"] = recipient_email

    body = "Hello World!"

    message.set_content(body)
    return message


def connect_smtp():
    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    return smtp


def trigger_alert():
    email_list = RESTOCK_EMAIL_LIST.split(",") if RESTOCK_EMAIL_LIST else []
    smtp_session = connect_smtp()

    try:
        send_multiple_emails(smtp_session, email_list)
    finally:
        smtp_session.quit()
