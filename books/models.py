from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

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
    cover_image = models.ImageField(upload_to=book_dir_path, blank=True)
    pdf_file = models.FileField(upload_to=book_dir_path, blank=True)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def is_new(self, threshold_days=7):
        cuttoff = timezone.now() + timedelta(days=threshold_days)
        return self.date_posted <= cuttoff

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def set_finish_time(self):
        # Change the finish date
        self.finish_date = self.start_date + timedelta(minutes=2) 
        self.save()

    @property
    def remaining_time(self):
        if self.finish_date:
            time_remaining = self.finish_date - timezone.now()
            # getting total seconds
            return int(time_remaining.total_seconds() / 60)
        return None

    def mark_as_complete(self):
        self.is_completed = True
        self.finish_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.username} Progress"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, related_name="reviews" ,on_delete=models.DO_NOTHING)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed by {self.user.username}"