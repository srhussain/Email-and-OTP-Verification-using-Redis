import random
from django.core.cache import cache
from django.core.mail import send_mail
import uuid
from django.conf import settings


def send_otp_to_mobile(mobile,user_obj):
    if cache.get(mobile):
        return False,cache.ttl(mobile)
    try:
        otp_to_sent=random.randint(1000,9999)
        cache.set(mobile,otp_to_sent, timeout=60)
        user_obj.otp=otp_to_sent
        user_obj.save()
        return True,0
    except Exception as e:
        print(e)

def send_email_token(email,user_obj):
    try:
        subject="Your email needs to be verified"
        token=uuid.uuid4()
        message= f"Hi, click on the link to verify email http://127.0.0.1:8000/accounts/verifyemail/{token}/"
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message,email_from,recipient_list)
        user_obj.email_token=token
        user_obj.save()
        

    except Exception as e:
            print(e)

def send_forgetPassword_token(email,user_obj):
    try:
        subject="Your Forget Password Link "
        token=str(uuid.uuid4())
        message= f"Hi, click on the link to reset your Password http://127.0.0.1:8000/accounts/change-password/{token}/"
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(subject,message,email_from,recipient_list)
        user_obj.forget_password_token=token
        user_obj.save()
        return True
        

    except Exception as e:
            print(e)