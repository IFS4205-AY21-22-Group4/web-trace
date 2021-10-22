# Generated by Django 3.2.7 on 2021-09-26 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("official", "0008_closecontact_cluster"),
    ]

    operations = [
        migrations.AddField(
            model_name="positivecases",
            name="cluster",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="official.cluster",
            ),
            preserve_default=False,
        ),
    ]