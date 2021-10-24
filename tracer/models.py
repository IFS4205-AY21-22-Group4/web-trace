# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User, BaseUserManager
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from knox.models import AuthToken
from Staff_Accounts.models import Staff, User, UserManager
from issuer.models import Token, MedicalRecord, Identity

<<<<<<< HEAD
from official.models import Cluster, PositiveCases, CloseContact
=======

class Cluster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField()

    class Meta:
        db_table = "cluster"


class PositiveCases(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT)
    date_test_positive = models.DateField()
    is_recovered = models.BooleanField()
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        db_table = "positivecases"


class Role(models.Model):
    name = models.CharField(unique=True, max_length=20)
    default_role = models.CharField(max_length=20, blank=True, null=True)
    permssions = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Role"


class CloseContact(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT)
    positivecase = models.ForeignKey(PositiveCases, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        db_table = "closecontact"
>>>>>>> 1ed34267d219ab74ed5e1ea18653b3520e3b07c4
