from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/',Login.as_view()),
    path('register/',RegisterView.as_view()),
    path('forget-password/',ForgetPassword.as_view()),
    path('change-password/<token>/',ChangePassword.as_view()),
    path('verifyotp/',VerifyOtp.as_view()),
    path('verifyemail/<token>/',Verifyemail.as_view()),
]