from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Favourite
from books.models import Book, Category

# Favorite test case
class TestFavourites(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="Test User",
            email="test@example.com",
            password="testpassword",
        )
        cls.category = Category.objects.create(
            title="Test Category"
        )

        cls.book = Book.objects.create(
            category=cls.category,
            author="Test Author",
            title="Test Book Title"
        )

        cls.favourite = Favourite.objects.create(
            user=cls.user,
            book=cls.book,
        )

    def test_favourite_contents(self):
        self.assertEqual(self.user, self.favourite.user)
        self.assertEqual(self.book, self.favourite.book)
        self.assertEqual(Favourite.objects.count(), 1)
        self.assertEqual(str(self.favourite), f'{self.user.username} favourite books')
