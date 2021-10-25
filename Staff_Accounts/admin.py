# from Staff_Accounts.models import CustomUser
from django.contrib.admin.decorators import register
from django.contrib.auth.models import User
from Staff_Accounts.models import Staff
from django.contrib import admin

# Register your models here.
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "roles",
        "email_validated",
        "is_verified",
        "number_of_attempts",
    )
    list_filter = ("roles", "is_verified")
    exclude = ("activation_key", "most_recent_otp")


admin.site.register(Staff, StaffAdmin)
