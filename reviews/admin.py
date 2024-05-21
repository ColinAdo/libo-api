from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "book",
        "date",
    ]


admin.site.register(Review, ReviewAdmin)
