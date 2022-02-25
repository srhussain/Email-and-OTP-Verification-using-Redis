from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=14)
    otp=models.CharField(max_length=6,null=True,blank=True)
    is_phone_verified=models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    forget_password_token=models.CharField(max_length=100,null=True,blank=True)
    last_login_time=models.DateTimeField(null=True,blank=True)
    last_logout_time=models.DateTimeField(null=True,blank=True)
    
    objects=UserManager()
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=[]

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


# class ForgetPassword(models.Model):
#     account=models.ForeignKey(User,on_delete=models.CASCADE)
#     forget_password_token=models.CharField(max_length=200,null=True,blank=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)


# 21o873-93287            ///UUID4
   
# @receiver(post_save,sender=User)
# def send_email_token(sender,instance,created,**kwargs):
#     if created:
#         try:
#             subject="Your email needs to be verified"
#             token=uuid.uuid4()
#             message= f"Hi, click on the link to verify email http://127.0.0.1:8000/accounts/verifyemail/{token}/"
#             email_from=settings.EMAIL_HOST_USER
#             recipient_list=[instance.email]
#             send_mail(subject,message,email_from,recipient_list)
#             user_obj=User.objects.get(email=instance.email)
#             user_obj.email_token=token
#             user_obj.save()
            

#         except Exception as e:
#             print(e)



