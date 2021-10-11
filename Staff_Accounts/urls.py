from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("", views.loginPage, name="login"),
    path("otp/", views.otp_verification, name="otp"),
    path("logout/", views.logoutUser, name="logout"),
    path("home/", views.home, name="home"),
    path("activate/account/", views.activate_account, name="activate_account"),
    path("reset/password/", views.reset_password, name="reset_password"),
]
