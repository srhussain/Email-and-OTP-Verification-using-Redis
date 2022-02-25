# import email

from lib2to3.pgen2 import token
from operator import truediv
from typing_extensions import Required

from .thready import *
from .helpers import *
from .models import *
from rest_framework import serializers
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password','phone']

    def create(self,validated_data):
        user=User.objects.create(email=validated_data['email'],phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        user.save()
        send_otp_to_mobile(user.phone,user)
        # send_email_token(user.email,user)
        token=str(uuid.uuid4())
        SendEmailVerification(user.email,token).start()
        user.email_token=token
        user.save()
        return user


        
        
        
        