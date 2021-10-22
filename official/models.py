from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from knox.models import AuthToken
from Staff_Accounts.models import UserManager, User, Staff


class SiteOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    postal_code = models.CharField(max_length=6)
    unit_no = models.CharField(max_length=6)

    class Meta:
        db_table = "siteowner"
        managed = False


class Identity(models.Model):
    nric = models.CharField(max_length=9, unique=True)
    fullname = models.CharField(max_length=100)
    address = models.TextField()
    phone_num = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = "identity"
        managed = False


class Token(models.Model):
    token_uuid = models.CharField(max_length=36)
    owner = models.ForeignKey(Identity, on_delete=models.PROTECT)
    issuer = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    hashed_pin = models.CharField(max_length=64)

    class Meta:
        db_table = "token"
        managed = False


class MedicalRecord(models.Model):
    identity = models.OneToOneField(Identity, on_delete=models.PROTECT)
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    vaccination_status = models.BooleanField(default=False)

    class Meta:
        db_table = "medicalrecords"
        managed = False


class Gateway(models.Model):
    gateway_id = models.CharField(max_length=15, unique=True)
    site_owner = models.ForeignKey(SiteOwner, on_delete=models.CASCADE)
    authentication_token = models.CharField(max_length=64, blank=False, null=True)

    def __str__(self):
        return self.gateway_id

    class Meta:
        db_table = "gateway"
        managed = False


class GatewayRecord(models.Model):
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "gatewayrecord"
        managed = False


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        User, related_name="logged_in_user", on_delete=models.CASCADE
    )
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "login_staff"
        managed = False


class Cluster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField()

    class Meta:
        db_table = "cluster"
        managed = True


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
        managed = True


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
        managed = True


class Edge(models.Model):
    id = models.BigAutoField(primary_key=True)
    vertex1_id = models.BigIntegerField()
    vertex1_category = models.CharField(
        max_length=20,
        choices=[("positive", "positive case"), ("contact", "close contact")],
    )
    vertex2_id = models.BigIntegerField()
    vertex2_category = models.CharField(
        max_length=20,
        choices=[("positive", "positive case"), ("contact", "close contact")],
    )
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)

    class Meta:
        db_table = "edge"
        managed = True
