from django.contrib import admin

from .models import LikeReview


class LikeReviewAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "review",
        "date",
    ]


admin.site.register(LikeReview, LikeReviewAdmin)
