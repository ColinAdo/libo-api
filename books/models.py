from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Book directory path
def book_dir_path(instance, filename):
    return "book/{0}/{1}".format(instance.author, filename)

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Book(models.Model):
    category = models.ForeignKey(Category, related_name="books", on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes", blank=True)
    readers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="readers", blank=True)
    cover_image = models.ImageField(upload_to=book_dir_path, blank=True)
    pdf_file = models.FileField(upload_to=book_dir_path, blank=True)
    description = models.TextField()
    text_content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def is_new(self, threshold_days=7):
        cuttoff = timezone.now() + timedelta(days=threshold_days)
        return self.date_posted <= cuttoff

    def __str__(self):
        return self.title
