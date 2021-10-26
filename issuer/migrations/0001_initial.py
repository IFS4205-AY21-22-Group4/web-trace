# Generated by Django 3.2.7 on 2021-10-26 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Staff_Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nric', models.CharField(max_length=9, unique=True)),
                ('fullname', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_num', models.CharField(max_length=8, unique=True)),
            ],
            options={
                'db_table': 'identity',
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_uuid', models.CharField(max_length=36)),
                ('status', models.BooleanField(default=True)),
                ('hashed_pin', models.CharField(max_length=64)),
                ('issuer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Staff_Accounts.staff')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='issuer.identity')),
            ],
            options={
                'db_table': 'token',
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccination_status', models.BooleanField(default=False)),
                ('identity', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='issuer.identity')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='issuer.token')),
            ],
            options={
                'db_table': 'medicalrecords',
            },
        ),
    ]
