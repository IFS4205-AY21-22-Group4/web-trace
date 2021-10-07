from django.contrib.auth.models import User
from django.forms.widgets import EmailInput, PasswordInput, Widget

# from Staff_Accounts.models import CustomUser, Staff
from Staff_Accounts.models import Staff
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


# User form for Registration
# class CreateUserForm(UserCreationForm):
#    class Meta:
#        model = CustomUser
#        fields = ["username", "email", "password1", "password2", "roles"]


class CreateUserForm(UserCreationForm):
    roles = forms.CharField(max_length=25, label="Roles")

    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2", "roles"]


# User form for OTP
class CreateUserOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
