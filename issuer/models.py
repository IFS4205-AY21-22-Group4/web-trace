from django.db import models

from django.contrib.auth.models import AbstractUser, Group, User, BaseUserManager
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from knox.models import AuthToken
from Staff_Accounts.models import Staff, User, UserManager


class Identity(models.Model):
    nric = models.CharField(max_length=9, unique=True)
    fullname = models.CharField(max_length=100)
    address = models.TextField()
    phone_num = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = "identity"


class Token(models.Model):
    token_uuid = models.CharField(max_length=36)
    owner = models.ForeignKey(Identity, on_delete=models.PROTECT)
    issuer = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    hashed_pin = models.CharField(max_length=128)

    class Meta:
        db_table = "token"


class MedicalRecord(models.Model):
    identity = models.OneToOneField(Identity, on_delete=models.PROTECT)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    vaccination_status = models.BooleanField(default=False)

    class Meta:
        db_table = "medicalrecords"
