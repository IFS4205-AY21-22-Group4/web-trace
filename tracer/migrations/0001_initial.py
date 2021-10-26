# Generated by Django 3.2.7 on 2021-10-26 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Staff_Accounts", "0001_initial"),
        ("issuer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                (
                    "default_role",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("permssions", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                "db_table": "Role",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Cluster",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("status", models.BooleanField()),
            ],
            options={
                "db_table": "cluster",
            },
        ),
        migrations.CreateModel(
            name="PositiveCases",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("date_test_positive", models.DateField()),
                ("is_recovered", models.BooleanField()),
                (
                    "cluster",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracer.cluster",
                    ),
                ),
                (
                    "identity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="issuer.identity",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Staff_Accounts.staff",
                    ),
                ),
            ],
            options={
                "db_table": "positivecases",
            },
        ),
        migrations.CreateModel(
            name="CloseContact",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "cluster",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracer.cluster",
                    ),
                ),
                (
                    "identity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="issuer.identity",
                    ),
                ),
                (
                    "positivecase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracer.positivecases",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="Staff_Accounts.staff",
                    ),
                ),
            ],
            options={
                "db_table": "closecontact",
            },
        ),
    ]
