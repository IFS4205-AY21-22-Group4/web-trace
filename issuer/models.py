# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# Create your models here.
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


#old
# class Medicalrecords(models.Model):
#    token = models.ForeignKey("Token", models.DO_NOTHING, blank=True, null=True)
#   identity = models.ForeignKey(Identity, models.DO_NOTHING, blank=True, null=True)
#    vaccination_status = models.CharField(max_length=20, blank=True, null=True)

#    class Meta:
#        managed = False
#       db_table = "MedicalRecords"
class Token(models.Model):
    token_uuid = models.CharField(max_length=36)
    owner = models.ForeignKey(Identity, on_delete=models.PROTECT)
    issuer = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    hashed_pin = models.CharField(max_length=64)

    class Meta:
        db_table = "token"

class MedicalRecord(models.Model):
    identity = models.OneToOneField(Identity, on_delete=models.PROTECT)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    vaccination_status = models.BooleanField(default=False)

    class Meta:
        db_table = "medicalrecords"

#class Role(models.Model):
#    name = models.CharField(unique=True, max_length=20)
#    default_role = models.CharField(max_length=20, blank=True, null=True)
#    permssions = models.CharField(max_length=20, blank=True, null=True)

#    class Meta:
#        managed = False
#        db_table = "Role"


#class Staff(models.Model):
#    username = models.CharField(unique=True, max_length=20)
#    password = models.CharField(max_length=20)
#    active = models.CharField(max_length=5, blank=True, null=True)
    # role_name = models.ForeignKey(Role, models.DO_NOTHING, db_column='role_name')
#    role_name = models.CharField(max_length=20)
#    email = models.CharField(max_length=20)

#    class Meta:
#        managed = False
#        db_table = "Staff"


#old
# class Token(models.Model):
#    token_serial_number = models.CharField(max_length=14)
#    identity = models.ForeignKey(Identity, models.DO_NOTHING)
#    staff_id = models.IntegerField()
#   status = models.IntegerField()
#    hashed_pin = models.CharField(max_length=128)

#    class Meta:
#        managed = False
#        db_table = "Token"






