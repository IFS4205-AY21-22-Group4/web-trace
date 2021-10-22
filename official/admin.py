from django.contrib import admin

# Register your models here.
from .models import Identity, PositiveCases, Cluster, CloseContact, Edge

admin.site.register([Identity, PositiveCases, Cluster, CloseContact, Edge])
