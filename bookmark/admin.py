from django.contrib import admin

from .models import Bookmark

# Favourite admin
class BookmarkAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'book',
        'created_at'
    ]

admin.site.register(Bookmark, BookmarkAdmin)
