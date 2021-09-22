import logging

###python manage.py create_groups to create groups
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ["Administrators", "Officials", "Contact Tracers", "Token Issuer"]


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
        print("Created default groups")
