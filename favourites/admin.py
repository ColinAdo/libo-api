from django.contrib import admin

from .models import Favourite

# Favourite admin
class FavouriteAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'book',
        'created_at'
    ]

admin.site.register(Favourite, FavouriteAdmin)
