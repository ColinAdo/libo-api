from django.conf import settings
from django.db import models

from books.models import Book


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.DO_NOTHING)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reviewed by {self.user.username}"
