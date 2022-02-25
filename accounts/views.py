from urllib import request
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .helpers import *
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from .thready import *


# Create your views here.


class Login(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            # email=data.get('email')
            # password=data.get('password')
            if serializer.is_valid():
                email=serializer.data['email']
                password=serializer.data['password']
                user = authenticate(email=email, password=password)
                if user is None:
                    return Response({
                        'status':404,
                        'message':'Invalid Password',
                        'data':{}
                    })

                if user.is_email_verified is False:
                    return Response({
                        'status':404,
                        'message':'Your account is not Verified ',
                        'data':{}
                    })


                refresh=RefreshToken.for_user(user)
                return Response({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)

                })


            return Response({
                'status':404,
                'message':'something went wrong',
                'data':serializer.errors
            })

            # if not email or not password:
            #      return Response({
            #     'status':404,
            #     'error':'Both username and password required'
            #     })
            # user_obj=User.objects.filter(email=email).first()
            # if user_obj is None:
            #      return Response({
            #     'status':404,
            #     'error':'User Not Found 1'
            #     })
            # if user is None:
            #      return Response({
            #     'status':404,
            #     'error':'Your Password is wrong !'
            #     })

            # login(request,user)
            # return Response({
            #     'status':200,
            #     'Message':'User Logged In Successfully !'
            #     })


        except Exception as e:
                print(e)
                return Response({
                    'status':404,
                    'error':'something went wrong'
                })



class RegisterView(APIView):

    def post(self,request):
        try:
            serializer=UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status':403,
                    'errors':serializer.errors

                })
            serializer.save()
            return Response({
                'status':200,
                'message':'An email sent on your Number and Email'
            })

        except Exception as e:
            print(e)
            return Response({
                'status':404,
                'error':'something went wrong'
            })

        


class Verifyemail(APIView):
    def get(self,request,token):
        try:
            user_obj=User.objects.filter(email_token=token).first()
            if user_obj:
                if user_obj.is_email_verified:
                    return Response({
                    'status':200,
                    'message':'Your account has been already verified',
                    # 'data':serializer.data,
                    })
                user_obj.is_email_verified=True
                user_obj.save()
                return Response({
                    'status':200,
                    'message':'Your account has been verified',
                    # 'data':serializer.data,
                    })
            else:
                return Response({
                    'status':404,
                    'message':'Error',
                    # 'data':serializer.data,
                    })

        
        except Exception as e:
            print(e)
            return Response({
                    'status':404,
                    'message':'ERROR 404',
                    # 'data':serializer.data,
                    })
    # def patch(self,request):
    #     try:
    #         data=request.data
    #         user_obj=User.objects.filter(email=data.get('email'))
    #         if not user_obj.exists():
    #             return  Response({
    #             'status':404,
    #             'message':'No User Found !'
    #             })
    #         status,time=send_email_token(data.get('email'),user_obj[0])
    #         if status:
    #             return Response({
    #             'status':200,
    #             'message':'New Email sent'
    #             })
    #         return Response({
    #             'status':404,
    #             'error':f'try after few seconds {time}'
    #             })

    #     except Exception as e:
    #         print(e)
    #     return Response({
    #             'status':404,
    #             'error':'Something went wrong'
    #             })


class VerifyOtp(APIView):
    def post(self,request):
        try:
            data=request.data
            user_obj=User.objects.get(phone=data.get('phone'))
            otp=data.get('otp')

            if user_obj.otp==otp:
                user_obj.is_phone_verified=True
                user_obj.save()
                return Response({
                'status':202,
                'message':'Your Otp is Verified'
                })
            return Response({
                'status':404,
                'message':'Your Otp is Wrong'
                })

        except Exception as e:
            print(e)
        return Response({
                'status':404,
                'error':'something went wrong'
            })

    def patch(self,request):
        try:
            data=request.data
            user_obj=User.objects.filter(phone=data.get('phone'))
            if not user_obj.exists():
                return  Response({
                'status':404,
                'message':'No User Found !'
                })
            status,time=send_otp_to_mobile(data.get('phone'),user_obj[0])
            if status:
                return Response({
                'status':200,
                'message':'New OTP sent'
                })
            return Response({
                'status':404,
                'error':f'try after few seconds {time}'
                })

        except Exception as e:
            print(e)
        return Response({
                'status':404,
                'error':'Something went wrong'
                })


class ForgetPassword(APIView):
    def post(self,request):

        try:
            data=request.data
            email=data.get('email')
            if not User.objects.filter(email=email).first():
                return Response({
                'status':404,
                'error':'No User Found with this username'
                })
            user_obj=User.objects.get(email=email)
            token=str(uuid.uuid4())
            # send_forgetPassword_token(user_obj.email,user_obj)
            SendForgetPasswordEmail(user_obj.email,token).start()
            user_obj.forget_password_token=token
            user_obj.save()
            return Response({
                'status':200,
                'message':'A Link  has sent to your Email Id '
            })

        except Exception as e:
            print(e)
            return Response({
                'status':404,
                'error':'something went wrong'
            })

class ChangePassword(APIView):
    def post(self,request,token):
        context={}
        try:
            user_obj=User.objects.filter(forget_password_token=token).first()
            print(user_obj)
            data=request.data
            new_password=data.get('new_password')
            confirm_password=data.get('confirm_password')
            # context={'user_id':user_obj.user.id}
            if new_password!=confirm_password:
                return Response({
                'status':404,
                'message':'Both Password are not same'
                })
            user_obj.set_password(new_password)
            user_obj.save()
            return Response({
                'status':200,
                'message':'Your Password has been changed Succesfully !'
                })



        except Exception as e:
            print(e)
        return Response({
                'status':404,
                'message':"ERROR 404"
            })
