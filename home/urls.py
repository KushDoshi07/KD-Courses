from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home , name='home'),
    path('about', views.about , name='about'),
    path('courses', views.courses , name='courses'),
    path('contact', views.contact , name='contact us'),
    path('login', views.loginUser , name='login'),
    path('after_login', views.after_login , name='after_login'),
    path('signup', views.signup , name='signup'),
    path('logout' , views.logoutUser , name='logoutUser'),
    path('forgot-password' , views.forgot_password , name='forgotpassword'),
    path('otp-verification' , views.emailverification , name='emailverification'),
    path('verify-otp' , views.verify_otp , name='verify-otp'),
    path('password-reset', views.password_reset, name='password_reset')
]