from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from books.models import Book, Category
from books.api.serializers import BookSerializer


class BookApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        cls.category = Category.objects.create(
            title="Test Category"
        )
        cls.book = Book.objects.create(
            category=cls.category,
            author="Test Author",
            title="Test Title",
        )

        cls.access_token = AccessToken.for_user(cls.user)

    def test_post_books(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse("books")

        data = {
            "category": self.category.id,
            "author": "Test Author2",
            "title": "Test Title2"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_get_books(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse("books")
        response = self.client.get(url, format='json')

        queryset = Book.objects.all()
        expected_data = BookSerializer(queryset, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_books(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse("book_detail", kwargs={'pk': self.book.id})
        response = self.client.get(url, format='json')

        obj = Book.objects.get(id=self.book.id)
        expected_data = BookSerializer(obj).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
