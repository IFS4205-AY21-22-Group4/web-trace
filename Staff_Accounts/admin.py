# from Staff_Accounts.models import CustomUser
from django.contrib.admin.decorators import register
from django.contrib.auth.models import User
from Staff_Accounts.models import Staff
from django.contrib import admin

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Staff, UserAdmin)
