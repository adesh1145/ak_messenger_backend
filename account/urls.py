
from django.contrib import admin
from django.urls import path,include
from account.views import UserChangePasswordView, UserOTPView, UserProfileView, UserRegistrationView,UserLoginView

 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('registration/',UserRegistrationView.as_view()),
    path('otp/',UserOTPView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('changepassword/',UserChangePasswordView.as_view()),
   
]
