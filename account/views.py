from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserChangePasswordSerializer, UserForgetSerializer, UserOTPSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from account.renderers import UserRenderer
from account.models import User


# OTP Genarate
def otpGenerator():
    return "1145"

# Generate Manually Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        request.data['otp'] = otpGenerator()
        # print(request.user)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()
            return Response({'msg': 'OTP Has Been Sent', 'link': 'otp/', 'email': request.data['email'], 'password': request.data['password']}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserOTPView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            password = request.data['password']
            otpByUser = request.data['otp']
            user = authenticate(email=email, password=password)
            if user is not None:
                userDetail = User.objects.get(email=user)
                # print(userDetail.otp)
                if otpByUser != userDetail.otp:
                    return Response({'error': {'msg': 'Invalid OTP'}}, status=status.HTTP_404_NOT_FOUND)
                else:
                    userDetail.is_verified = True
                    userDetail.save()
                    return Response({'msg': 'OTP Verified'}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'error': {'msg': 'Invali Email or Password'}}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'error': {'msg': 'Bad Request'}}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data['password']
            # is_verified=True
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                userDetail = User.objects.filter(email=email).values()[
                    0].get('is_verified')
                if userDetail:
                    loginToken = get_tokens_for_user(user)
                    return Response({'msg': 'successful login', 'token': loginToken}, status=status.HTTP_200_OK)
                else:
                    return Response({'link': 'otp/', 'email': email, 'password': password}, status=status.HTTP_200_OK)

            else:
                return Response({'error': {'email': ['Invalid Email or Password']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class UserForgetView(APIView):

    def post(self, request, format=None):
        print(request.data)
        # request.data['otp']="4545"
        serializer = UserForgetSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):

                email = request.data['email']
                userDetail = User.objects.get(email=email)
                if userDetail.email is not None:
                    otp=otpGenerator()
                    otp="1146"
                    userDetail.otp=otp
                    userDetail.save()
                    return Response({'msg': 'OTP Sent'}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'error': {'msg': ['Invalid Email']}}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': {'msg': ['Bad Request ']}}, status=status.HTTP_404_NOT_FOUND)
            
        except:
                return Response({'error': {'msg': ['Invalid Email']}}, status=status.HTTP_400_BAD_REQUEST)

class UserForgetOTPView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        # try:
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            otpByUser=request.data.get('otp')
            password=request.data.get('password')
            print(email,otpByUser,password)
            userDetail=User.objects.get(email=email)
            print(userDetail.otp)
            if userDetail.email is None:
                return Response({'error': {'msg': ['Invalid Email']}}, status=status.HTTP_404_NOT_FOUND)
            elif userDetail.otp!=otpByUser:
                return Response({'error': {'msg': ['Invalid OTP']}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            userDetail.set_password(password)
            userDetail.is_verifeid=True
            userDetail.save()
            return Response( {'msg': 'Password Changed'}, status=status.HTTP_205_RESET_CONTENT)
        # except:
        #     return Response({'error': {'msg': 'Bad Request'}}, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
