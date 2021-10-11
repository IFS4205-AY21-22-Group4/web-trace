from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class CreateUserForm(UserCreationForm):
    roles = forms.CharField(max_length=25, label="Roles")

    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2", "roles"]


# User form for OTP
class CreateUserOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)


class CreatePasswordResetForm(forms.Form):
    email = forms.EmailField()
