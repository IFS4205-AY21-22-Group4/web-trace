from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    roles = models.CharField(max_length=20, blank=True)
