
from django.contrib import admin
from django.urls import path,include
from account.views import UserChangePasswordView, UserForgetOTPView, UserForgetView, UserOTPView, UserProfileView, UserRegistrationView,UserLoginView

 

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/',UserRegistrationView.as_view()),
    path('otp/',UserOTPView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('forget/',UserForgetView.as_view()),
    path('forget_otp/',UserForgetOTPView.as_view()),
    path('profile/',UserProfileView.as_view()),
    path('change_password/',UserChangePasswordView.as_view()),

   
]
