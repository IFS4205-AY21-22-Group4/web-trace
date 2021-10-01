from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django.db.models.base import Model

# Custom User for Login
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.CharField(max_length=20, blank=True)
    activation_key = models.CharField(
        max_length=255, default=1
    )  # link for email verification
    most_recent_otp = models.CharField(
        max_length=6, blank=True
    )  # value for otp verification
    email_validated = models.BooleanField(default=False)  # verify email inputted
    is_verified = models.BooleanField(default=False)  # verify otp inputted
