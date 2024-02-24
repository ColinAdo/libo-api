from django.conf import settings
from django.db import models

def book_dir_path(instance, filename):
    return "book/{0}/{1}".format(instance.title, filename)


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Book(models.Model):
    category = models.ForeignKey(Category, related_name="books", on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    favourites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="favourite", blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)
    readers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="readers", blank=True)
    cover_image = models.ImageField(upload_to=book_dir_path)
    pdf_file = models.FileField(upload_to=book_dir_path)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
