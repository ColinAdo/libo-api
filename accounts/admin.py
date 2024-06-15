from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser

# Custom user admin
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = [
        "username", 
        "email", 
        "display_image",
        "is_staff", 
        "is_superuser"
    ]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.profile_picture.url, obj.profile_picture.url))
    display_image.short_description = 'Profile picture'

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("profile_picture",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("profile_picture",)}),)

admin.site.register(CustomUser, CustomUserAdmin)

