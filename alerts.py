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


def send_multiple_emails(smtp, email_list, product):
    for email in email_list:
        try:
            send_email(smtp, email, product)
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")


def send_email(smtp, email, product):
    email_message = create_email_message(email, product)
    smtp.send_message(email_message)


def create_email_message(recipient_email, product):
    name, color, capacity, url = (
        product.get("name"),
        product.get("color"),
        product.get("capacity"),
        product.get("url"),
    )

    message = EmailMessage()
    message["Subject"] = f"🚨 Back In Stock: {color} {name} ({capacity})"
    message["From"] = f"Restock Alert <{SMTP_USER}>"
    message["To"] = recipient_email

    body = (
        f"Great news!\n\n"
        f"The {color.lower()} {name} ({capacity}) you've been waiting for is back in stock!\n\n"
        f"To purchase, click the link below:\n\n"
        f"{url}"
    )

    message.set_content(body)
    return message


def connect_smtp():
    smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    return smtp


def trigger_alert(product):
    email_list = RESTOCK_EMAIL_LIST.split(",") if RESTOCK_EMAIL_LIST else []
    smtp_session = None

    try:
        smtp_session = connect_smtp()
        send_multiple_emails(smtp_session, email_list, product)
    finally:
        if smtp_session is not None:
            smtp_session.quit()
