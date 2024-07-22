from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField

# user directory path
def user_directory_path(instance, filename):
    return "profile/{0}/{1}".format(instance.username, filename)

characters = "abcdefghijklmnopqrstuvwxyz0123456789ABCDFGHIJKLMNOPQRSTUVWXYZ"

#  Custom user model
class CustomUser(AbstractUser):
    profId = ShortUUIDField(unique=True, length=10, max_length=20, alphabet=characters)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    profile_picture = models.ImageField(default='profile.png', upload_to=user_directory_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
