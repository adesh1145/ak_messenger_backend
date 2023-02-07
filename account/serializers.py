from account.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        password2 = serializers.CharField(style={'input_type': 'password'},
                                          write_only=True)
        model = User
        fields = ['email', 'number', 'name', 'password', 'otp']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        email=data.get('email')
        number=data.get('number')
        print(User.objects.filter(email=email).values()[0].get('otp'))
        print(User.objects.filter(email=email).values())
        if User.objects.filter(email=email).exists() and User.objects.filter(email=email).values()[0].get('is_verified') ==1:
            print("yes")
            raise serializers.ValidationError("Email is Already Registered")
        elif User.objects.filter(number=number).exists() and User.objects.filter(number=number).values()[0].get('is_verified') ==1:
            print("y")
            raise serializers.ValidationError("Number is Already Registered")

        
        return data
    
    def create(self, validated_data):
        email=validated_data['email']
        number=validated_data['number']
        print("email",email)
        if User.objects.filter(email=email).exists() and User.objects.filter(email=email).values()[0].get('is_verfied')==False:
            print("update")
            return User.objects.update_unverified_data(validated_data['email'], validated_data['number'], validated_data['name'], validated_data['password'], validated_data['otp'])
        elif User.objects.filter(number=number).exists() and User.objects.filter(number=number).values()[0].get('is_verified')==False:
            return User.objects.update_unverified_data(validated_data['email'], validated_data['number'], validated_data['name'], validated_data['password'], validated_data['otp'])
            
        return User.objects.create_user(validated_data['email'], validated_data['number'], validated_data['name'], validated_data['password'], validated_data['otp']) 


    

class UserOTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6)

    class Meta:
        model = User
        fields = ['otp']
    def validate(self, attrs):
        otpByUser=attrs.get('otp')
        user = self.context.get('user')
        userDetail=User.objects.filter(email=user).values()
        print("oto=",userDetail[0].get('otp'))
        if otpByUser!=userDetail[0].get('otp'):
           raise serializers.ValidationError(
                "Invalid OTP")
       
        user.is_verified=True
        user.save()
        return attrs

class UserLoginSerializer(serializers.ModelSerializer):
    # def __init__(email,password):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password',]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'number', 'name', 'description']
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
