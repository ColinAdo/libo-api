from django.contrib import admin

from .models import Progress

# Progress admin
class ProgressAdmin(admin.ModelAdmin):
    list_display = [
        "book",
        "user",
        "start_date",
        "finish_date",
        "is_completed",
    ]


admin.site.register(Progress, ProgressAdmin)
