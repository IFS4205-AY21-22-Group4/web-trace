from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django.db.models.base import Model

# Create your models here.
class CustomUser(AbstractUser):
    roles = models.CharField(max_length=20, blank=True)
    activation_key = models.CharField(max_length=255, default=1)
    most_recent_otp = models.CharField(max_length=6, blank=True)
    # email_validated = models.BooleanField(default=False)
