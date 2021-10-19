from django.db import models

# Create your models here.
class Identity(models.Model):
    id = models.BigAutoField(primary_key=True)
    nric = models.CharField(max_length=9)
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_num = models.CharField(max_length=8)

    def __str__(self):
        return "id: %s, nric: %s, fullname: %s, address: %s, phone_num: %s" % (
            self.id,
            self.nric,
            self.fullname,
            self.address,
            self.phone_num,
        )

    class Meta:
        managed = True


class Role(models.Model):
    name = models.CharField(max_length=20)
    default = models.CharField(max_length=20)
    permissions = models.CharField(max_length=20)

    def __str__(self):
        return "name: %s, default: %s, permissions: %s" % (
            self.name,
            self.default,
            self.permissions,
        )

    class Meta:
        managed = True


class Staff(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    active = models.BooleanField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    email = models.CharField(max_length=20)

    def __str__(self):
        return "id: %s, username: %s, role: %s" % (
            self.id,
            self.username,
            self.role.name,
        )

    class Meta:
        managed = True


class Cluster(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    status = models.BooleanField()

    def __str__(self):
        return "id: %s, name: %s, status: %s" % (
            self.id,
            self.name,
            "active" if self.status else "inactive",
        )

    class Meta:
        managed = True


class PositiveCases(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE)
    date_test_positive = models.DateField()
    is_recovered = models.BooleanField()
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return "id: %s, identity_id: %s, date_test_positive: %s, is_recovered: %s, staff_id: %s" % (
            self.id,
            self.identity,
            self.date_test_positive,
            self.is_recovered,
            self.staff,
        )

    class Meta:
        managed = True


class CloseContact(models.Model):
    id = models.BigAutoField(primary_key=True)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE)
    positivecase = models.ForeignKey(PositiveCases, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)

    def __str__(self):
        return "id: %s, identity_id: %s, positivecase: %s, staff_id: %s" % (
            self.id,
            self.identity,
            self.positivecase,
            self.staff,
        )

    class Meta:
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

    def __str__(self):
        return "id: %s, vertex1_id: %s, vertex1_category: %s, vertex2_id: %s, vertex_category: %s, cluster_id: %s" % (
            self.id,
            self.vertex1_id,
            self.vertex1_category,
            self.vertex2_id,
            self.vertex2_category,
            self.cluster,
        )

    class Meta:
        managed = True


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    token_serial_number = models.CharField(max_length=10)
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.BooleanField()
    hashed_pin = models.BigIntegerField()

    class Meta:
        managed = True


class Gateway(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = True


class GatewayRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        managed = True
