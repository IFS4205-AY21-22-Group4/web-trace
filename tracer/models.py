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

#class Closecontact(models.Model):
#    identity = models.ForeignKey("Identity", models.DO_NOTHING, blank=True, null=True)
#    positivecase_id = models.IntegerField(blank=True, null=True)
#    staff_id = models.IntegerField(blank=True, null=True)

#    class Meta:
#        managed = False
#        db_table = "CloseContact"


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

#class Medicalrecords(models.Model):
#    token = models.ForeignKey("Token", models.DO_NOTHING, blank=True, null=True)
#    identity = models.ForeignKey(Identity, models.DO_NOTHING, blank=True, null=True)
#    vaccination_status = models.CharField(max_length=20, blank=True, null=True)

#    class Meta:
#        managed = False
#        db_table = "MedicalRecords"

class Role(models.Model):
    name = models.CharField(unique=True, max_length=20)
    default_role = models.CharField(max_length=20, blank=True, null=True)
    permssions = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Role"


#class Staff(models.Model):
#    username = models.CharField(unique=True, max_length=20)
#    password = models.CharField(max_length=32, blank=True, null=True)
#    active = models.CharField(max_length=5, blank=True, null=True)
#    role_name = models.CharField(unique=True, max_length=20, blank=True, null=True)
#    email = models.CharField(max_length=20)

#    class Meta:
#        managed = False
#        db_table = "Staff"


#class Token(models.Model):
#    token_serial_number = models.CharField(max_length=10)
#    identity = models.ForeignKey(Identity, models.DO_NOTHING)
#    staff_id = models.IntegerField()
#    status = models.IntegerField()
#    hashed_pin = models.CharField(max_length=128, blank=True, null=True)

#    class Meta:
#        managed = False
#        db_table = "Token"




class CloseContact(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT)
    positivecase = models.ForeignKey(PositiveCases, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, blank=True, null=True)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "closecontact"
