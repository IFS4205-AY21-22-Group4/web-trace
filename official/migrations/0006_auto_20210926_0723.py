# Generated by Django 3.2.7 on 2021-09-26 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('official', '0005_auto_20210926_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='status',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='positivecases',
            name='is_recovered',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='staff',
            name='active',
            field=models.BooleanField(),
        ),
    ]
