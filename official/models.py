from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from knox.models import AuthToken
from Staff_Accounts.models import UserManager, User, Staff, LoggedInUser
from issuer.models import Identity, MedicalRecord, Token


class SiteOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, primary_key=True)
    postal_code = models.CharField(max_length=6)
    unit_no = models.CharField(max_length=6)

    class Meta:
        db_table = "siteowner"


class Gateway(models.Model):
    gateway_id = models.CharField(max_length=15, unique=True)
    site_owner = models.ForeignKey(SiteOwner, on_delete=models.CASCADE)
    authentication_token = models.CharField(max_length=64, blank=False, null=True)

    def __str__(self):
        return self.gateway_id

    class Meta:
        db_table = "gateway"


class GatewayRecord(models.Model):
    token = models.ForeignKey(Token, on_delete=models.PROTECT)
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "gatewayrecord"


class Cluster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField()

    class Meta:
        db_table = "cluster"
        managed = True

    def __str__(self):
        return "Cluster " + str(self.id) + ": " + str(self.name)


class PositiveCases(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.PROTECT)
    date_test_positive = models.DateField()
    is_recovered = models.BooleanField()
    staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
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
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "closecontact"
        managed = True

    def __str__(self):
        return str(self.id)


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
