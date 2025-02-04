from django.test import TestCase

from accounts.models import CustomUser
from books.models import Book, Category
from likes.models import Like

# Likes test case
class TestLikeReview(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
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

        cls.like = Like.objects.create(
            user=cls.user,
            book=cls.book
        )

    def test_like_post(self):
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.review, self.review)
        self.assertEqual(str(self.like), f'{self.user.username} likes')
