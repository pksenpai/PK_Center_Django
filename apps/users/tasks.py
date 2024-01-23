from celery import shared_task
from django.core.mail import send_mail
from conf import settings


@shared_task(bind=True)
def send_otp_by_email(self, email, otp): # has self in args
    mail_subject = "PK Center OTP"
    message = \
        "Welcome to PK Center!\n" \
        f"OTP Code: {otp}"
    
    to_email = email
    
    status = send_mail(
        subject= mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    
    return status
