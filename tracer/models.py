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
from official.models import Cluster, PositiveCases, CloseContact
