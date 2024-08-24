from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

from likes.models import LikeReview
from reviews.models import Review
from books.models import Book, Category 

# Like post api test case
class TestLikePost(APITestCase):
    
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
            title='Test Title'
        )

        cls.review = Review.objects.create(
            user=cls.user,
            book=cls.book,
            content='first review'
        )

        cls.like = LikeReview.objects.create(
            user=cls.user,
            review=cls.review
        )

        cls.access_token = AccessToken.for_user(cls.user)

    def test_like_post(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('like', kwargs={'pk': self.review.id})

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
