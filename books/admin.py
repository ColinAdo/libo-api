from django.contrib import admin
from django.utils.html import mark_safe

from .models import Category, Book

# Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

# Book admin
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'category', 
        'author', 
        'title', 
        'display_image',
        'read_pdf'
    ]

    def display_image(self, obj):
        return mark_safe('<a href="{}"> <img src="{}" width="30" height="30" style="border-radius: 50%;" /> </a>'.format(obj.cover_image, obj.cover_image))
    display_image.short_description = 'Cover Image'

    def read_pdf(self, obj):
        return mark_safe('<a href="{}"> READ IT </a>'.format(obj.pdf_file))
    read_pdf.short_description = 'File'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
