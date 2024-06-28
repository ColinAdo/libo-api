from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import UserSerializer

class ProfileApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com'
        )

        cls.access_token = AccessToken.for_user(cls.user)

    def test_retrieve_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('profile', kwargs={'profId': self.user.profId})
        response = self.client.get(url, format='json')

        profile = get_user_model().objects.get(profId=self.user.profId)
        expected_data = UserSerializer(profile).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
