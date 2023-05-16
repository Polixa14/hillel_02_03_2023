from django.core.mail import send_mail
from project.celery import app
from main.models import EmailConfig


@app.task
def send_mail_from_contact_form(email, message, subject):
    send_mail(
        subject=subject,
        message=message,
        from_email=email,
        recipient_list=[EmailConfig.load().contact_form_email]
    )
