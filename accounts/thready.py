import threading
from django.conf import settings
from django.core.mail import send_mail

class SendForgetPasswordEmail(threading.Thread):

    def __init__(self,email,token):
        self.email=email
        self.token=token
        threading.Thread.__init__(self)

    def run(self):
        try:
            subject="Your Forget Password Link "
            message= f"Hi, click on the link to reset your Password http://127.0.0.1:8000/accounts/change-password/{self.token}/"
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[self.email]
            send_mail(subject,message,email_from,recipient_list)
            return True
            

        except Exception as e:
                print(e)

class SendEmailVerification(threading.Thread):

    def __init__(self,email,token):
        self.email=email
        self.token=token
        threading.Thread.__init__(self)

    def run(self):
        try:
            subject="Your Forget Password Link "
            message= f"Hi, click on the link to verify your email http://127.0.0.1:8000/accounts/verifyemail/{self.token}/"
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[self.email]
            send_mail(subject,message,email_from,recipient_list)
            return True
            

        except Exception as e:
                print(e)