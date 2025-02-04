from django.contrib import admin

from .models import Like

# Like reviews admin
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'book',
        'date',
    ]


admin.site.register(Like, LikeAdmin)
