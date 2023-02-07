from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserChangePasswordSerializer, UserOTPSerializer, UserProfileSerializer, UserRegistrationSerializer,UserLoginSerializer
from account.renderers import UserRenderer
# Create your views here.

# OTP Genarate

def otpGenerator():
    return"1145"
# Generate Manually Token

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        request.data['otp']=otpGenerator()
        # print(request.data)
        serializer=UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            
            user=serializer.save()
            # print("User:",user)
            token=get_tokens_for_user(user)
            return Response({'msg':'OTP Sent',
            "token":token
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserOTPView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserOTPSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):

            return Response({'msg':'OTP Verified'},status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        



class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data['password']
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'msg':'successful login','token':token},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'msg':'Invali Email or Password'}},status=status.HTTP_404_NOT_FOUND)



class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)



class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):

        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        
        if serializer.is_valid(raise_exception=True):
            
            
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



