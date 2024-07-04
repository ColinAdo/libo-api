from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from progresses.models import Progress
from progresses.api.serializers import ProgressSerializer
from favourites.models import Favourite
from favourites.api.serializers import FavouriteSerializer
from books.models import Book, Category
from .serializers import UserSerializer

class ProfileApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com'
        )
        cls.other_user = User.objects.create(
            username='otheruser',
            email='otheruser@example.com'
        )
        cls.category = Category.objects.create(
            title="Test Category"
        )
        cls.book1 = Book.objects.create(
            category=cls.category,
            author="Test Author",
            title="Test Title",
        )
        cls.book2 = Book.objects.create(
            category=cls.category,
            author="Test Author two",
            title="Test Title two",
        )

        cls.access_token = AccessToken.for_user(cls.user)
        cls.other_access_token = AccessToken.for_user(cls.other_user)

        cls.reading_book = Progress.objects.create(user=cls.user, book=cls.book1, is_reading=True)
        cls.read_book = Progress.objects.create(user=cls.user, book=cls.book2, is_reading=False)
        cls.favourite_book = Favourite.objects.create(user=cls.user, book=cls.book2)

    def test_retrieve_owner_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('profile', kwargs={'profId': self.user.profId})
        response = self.client.get(url, format='json')

        User = get_user_model()
        profile = User.objects.get(profId=self.user.profId)
        reading_books = Progress.objects.filter(user=profile, is_reading=True)
        read_books = Progress.objects.filter(user=profile, is_reading=False)
        book_saved = Favourite.objects.filter(user=profile)

        reading_books_data = ProgressSerializer(reading_books, many=True).data
        read_books_data = ProgressSerializer(read_books, many=True).data
        book_saved_data = FavouriteSerializer(book_saved, many=True).data
        profile_data = UserSerializer(profile).data

        expected_data = {
            'profile': profile_data,
            'reading_books': reading_books_data,
            'read_books': read_books_data,
            'book_saved': book_saved_data
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_retrieve_other_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_access_token}')
        url = reverse('profile', kwargs={'profId': self.user.profId})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'You are not the owner...')