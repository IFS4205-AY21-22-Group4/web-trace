from Staff_Accounts.models import CustomUser
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "roles"]


class CreateUserOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
