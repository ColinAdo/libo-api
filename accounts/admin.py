from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser

# Custom user admin
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 
        'email', 
        'is_staff', 
        'is_superuser'
    ]

admin.site.register(CustomUser, CustomUserAdmin)

