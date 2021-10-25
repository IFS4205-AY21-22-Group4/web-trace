import logging

###python manage.py create_groups to create groups
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from config.settings import DB

db_logger = logging.getLogger(DB)

GROUPS = ["Administrators", "Officials", "Contact Tracers", "Token Issuers"]
PERMISSIONS = [
    "Can delete user",
    "Can view user",
    "Can delete staff",
    "Can view staff",
]


class Command(BaseCommand):
    help = "Creates read only default permission groups for users"

    def handle(self, *args, **options):
        db_logger.info("Create groups")
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            if group == "Administrators":
                for permission in PERMISSIONS:
                    model_add_perm = Permission.objects.get(name=permission)
                    new_group.permissions.add(model_add_perm)
        print("Created default groups")
