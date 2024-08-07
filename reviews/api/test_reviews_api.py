from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from reviews.models import Review
from books.models import Book, Category

# Rview api test case
class ReviewApiTestCase(APITestCase):
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
        cls.review = Review.objects.create(
            user=cls.user,
            book=cls.book,
            content='test content'
        )

        cls.access_token = AccessToken.for_user(cls.user)

    def test_perform_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('reviews-list')
        data = {
            "book": self.book.id,
            "content": "second review"
        }

        response = self.client.post(url, data, format='json')
        review = Review.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(review.user, self.user)

    def test_get_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url= reverse('reviews-list')

        response = self.client.get(url, format='json')
        query = Review.objects.all()
        expected_data = ReviewSerializer(query, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertContains(response, self.user)

    def test_retrieve_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})

        response = self.client.get(url)
        obj = Review.objects.get(pk=self.review.id)
        expected_data = ReviewSerializer(obj).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertContains(response, self.user)

    def test_update_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})

        data = {
            "user": self.user.id,
            "book": self.book.id,
            "content": "updated content"
        }
        response = self.client.put(url, data, format='json')
        self.review.refresh_from_db()


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.review.content, 'updated content')

    def test_delete_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('reviews-detail', kwargs={'pk': self.review.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)


# Is owner or read only test case
class IsOwnerOrReadOnlyTestCase(APITestCase):
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
            title='Test Category'
        )
        cls.book = Book.objects.create(
            category=cls.category,
            author='Test Author',
            title='Test Title',
        )
        cls.review = Review.objects.create(
            user=cls.user,
            book=cls.book,
            content='This is review content'
        )
        cls.permission = IsOwnerOrReadOnly()
        cls.view = APIView()
        cls.factory = APIRequestFactory()


    def test_safe_method_permission(self):
        request = self.factory.get('/')
        request.user = self.user

        self.assertTrue(self.permission.has_object_permission(request, self.view, self.review))

    def test_unsafe_method_permission_owner(self):
        request = self.factory.post('/')
        request.user = self.user

        self.assertTrue(self.permission.has_object_permission(request, self.view, self.review))

    def test_unsafe_method_permission_non_owner(self):
        request = self.factory.post('/')
        request.user = self.other_user

        self.assertFalse(self.permission.has_object_permission(request, self.view, self.review))