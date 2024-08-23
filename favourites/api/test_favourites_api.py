from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from favourites.models import Favourite
from books.models import Book, Category

# Favourite api test case
class TestFavourite(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        cls.category = Category.objects.create(
            title='Test Category'
        )
        cls.book = Book.objects.create(
            category=cls.category,
            author='Test Author',
            title='Test Title',
        )
        cls.favourite = Favourite.objects.create(
            user=cls.user,
            book=cls.book
        )
        cls.access_token = AccessToken.for_user(cls.user)

    def test_post_favourite(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('favourite', kwargs={'pk': self.book.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
