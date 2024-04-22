from django.db import models
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    return "profile/{0}/{1}".format(instance.username, filename)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    profile_picture = models.ImageField(default='profile.png', upload_to=user_directory_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
