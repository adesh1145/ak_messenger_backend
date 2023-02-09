from account.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['email', 'name', 'password', 'otp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        email = data.get('email')
        return data

    def create(self, validated_data):
        return User.objects.create_user(validated_data['email'], validated_data['name'], validated_data['password'], validated_data['otp'])


class UserOTPSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'otp']


class UserLoginSerializer(serializers.ModelSerializer):
    # def __init__(email,password):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password',]

class UserForgetSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ['email']

class UserForgetOTPSerializer(serializers.Serializer):

    class Mata:
        model= User
        fields=['email','otp','password']

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'description']
        # fields='__all__'


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'},
                                      write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attr):
        password = attr.get('password')
        password2 = attr.get('password2')
        user = self.context.get('user')

        if (password != password2):
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't Match")

        user.set_password(password)
        user.save()

        return attr
