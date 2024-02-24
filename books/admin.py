from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    display_list = ["title"]


admin.site.register(Category, CategoryAdmin)
