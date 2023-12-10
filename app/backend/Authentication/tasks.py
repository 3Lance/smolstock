from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from twilio.rest import Client
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import SignUpUser, Email_OTP, Two_Factor_OTP


@shared_task(bind = True)
def send_email_through_celery(self, subject, html_content, recepient):
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST,
            [recepient]
            )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return subject + ' EMAIL SENT'


@shared_task(bind = True)
def send_sms_through_celery(self, otp, recepient):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=f"Use the following OTP for smolstock Two Factor Authentication.\nOTP : {otp}, valid for only 2 minutes",
        from_=settings.TWILIO_DEFAULT_CALLERID,
        to=f"+91{recepient}"
    )
    return 'SMS SENT'


@shared_task(bind=True)
def delete_sign_up_users(self):
    users = SignUpUser.objects.all()
    for user in users:
        if user.token_generated_at + timedelta(minutes=15) < timezone.now():
            user.delete()
    return "DELETED SIGN UP USERS"


@shared_task(bind=True)
def delete_email_otps(self):
    otps = Email_OTP.objects.all()
    for otp in otps:
        if otp.created_time + timedelta(minutes=5) < timezone.now():
            otp.delete()
    return "DELETED EMAIL OTPs"


@shared_task(bind=True)
def delete_sms_otps(self):
    otps = Two_Factor_OTP.objects.all()
    for otp in otps:
        if otp.created_time + timedelta(minutes=2) < timezone.now():
            if not otp.phone_number.verified:
                otp.phone_number.delete()
            else:
                otp.delete()
    return "DELETED SMS OTPs"