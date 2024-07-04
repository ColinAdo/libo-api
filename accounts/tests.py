from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from .models import CustomUser
from core.authentication import CustomJWTAuthentication

import os

class CustomUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            username='testuser',
            email='testuser@example.com',
        )
        cls.test_file = SimpleUploadedFile('profile.png', b'file_content', content_type='image/png')

    def test_user_model_content(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(str(self.user), 'testuser')

    def test_user_directory_path(self):
        self.user.profile_picture = self.test_file
        self.user.save()

        stored_path = self.user.profile_picture.name
        directory, filename = os.path.split(stored_path)

        expected_directory = f'profile/{self.user.username}'

        self.assertEqual(directory, expected_directory)
        self.assertTrue(filename.startswith('profile'))

class CustomJWTAuthenticationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.auth = CustomJWTAuthentication()

        User = get_user_model()
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_authenticate_no_token(self):
        request = self.factory.get('/')

        request = self.auth.authenticate(request)

        self.assertIsNone(request)

    def test_authenticate_invalid_token(self):
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer invalidtoken'
        
        result = self.auth.authenticate(request)
        
        self.assertIsNone(result)