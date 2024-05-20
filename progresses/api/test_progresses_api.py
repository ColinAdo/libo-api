from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from progresses.api.serializers import ProgressSerializer
from progresses.models import Progress
from books.models import Book, Category

class TestProgress(APITestCase):
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
        cls.progress = Progress.objects.create(
            user=cls.user,
            book=cls.book
        )
        cls.access_token = AccessToken.for_user(cls.user)

    def test_post_progresses(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('progress-list')

        data = {
            "user": self.user.id,
            "book": self.book.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Progress.objects.count(), 2)

    def test_get_progress(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('progress-list')

        queryset = Progress.objects.all()
        expected_data = ProgressSerializer(queryset, many=True).data
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(len(response.data), 1)

