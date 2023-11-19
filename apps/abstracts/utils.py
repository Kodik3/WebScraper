from django.core.mail import EmailMessage
from django.conf import settings

def send_email(header: str, msg: str, to_emails: list) -> None:
    if not to_emails:
        print("Не указаны адреса электронной почты.")
        return
    result_header = f"| {settings.SITE_NAME} | " + header
    email = EmailMessage(result_header, msg, settings.EMAIL_FROM, to_emails)
    email.send()
