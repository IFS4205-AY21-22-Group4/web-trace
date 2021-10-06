from django.contrib import admin

# Register your models here.
from .models import Identity, Role, Staff, PositiveCases, Cluster, CloseContact, Edge

admin.site.register([Identity, Role, Staff, PositiveCases, Cluster, CloseContact, Edge])
