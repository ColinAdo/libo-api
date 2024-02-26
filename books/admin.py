from django.contrib import admin
from django.utils.html import mark_safe

from .models import Category, Book, Progress

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]

class BookAdmin(admin.ModelAdmin):
    list_display = [
        "category", 
        "author", 
        "title", 
        "display_image",
        "read_pdf"
    ]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.cover_image.url, obj.cover_image.url))
    display_image.short_description = 'Cover Image'

    def read_pdf(self, obj):
        return mark_safe('<a href="{}"> READ IT </a>'.format(obj.pdf_file.url))
    read_pdf.short_description = 'File'

class ProgressAdmin(admin.ModelAdmin):
    list_display = [
        "book",
        "user",
        "start_date",
        "finish_date",
        "is_completed",
    ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Progress, ProgressAdmin)
