from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            username='testuser',
            email='testuser@example.com',
        )

    def test_user_model_content(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(str(self.user), 'testuser')