from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book, Category
from .models import Review

# Review test case 
class ReviewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create(
            username="Test User",
            email="test@example.com",
            password="testpassword",
        )
        cls.category = Category.objects.create(
            title="Test Category"
        )

        cls.book = Book.objects.create(
            category=cls.category,
            author="Test Author",
            title="Test Book Title"
        )

        cls.review = Review.objects.create(
            user=cls.user,
            book=cls.book,
            content="Test Book Review"
        )

    def test_review_contents(self):
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.book, self.book)
        self.assertEqual(self.review.content, "Test Book Review")
        self.assertEqual(str(self.review), f"Reviewed by {self.user.username}")
