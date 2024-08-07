from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta

from books.models import Book

# Progress model
class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='progress',on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    is_reading = models.BooleanField(default=True, blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def set_finish_time(self):
        # Change the finish date
        self.finish_date = self.start_date + timedelta(minutes=1)
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
        return f'{self.user.username} Progress'
