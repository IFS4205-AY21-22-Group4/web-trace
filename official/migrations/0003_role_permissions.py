# Generated by Django 3.2.7 on 2021-09-25 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("official", "0002_remove_role_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="permissions",
            field=models.CharField(default="official", max_length=20),
            preserve_default=False,
        ),
    ]