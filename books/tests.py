from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Category, Book, Review

class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            title="Test Category"
        )

    def test_category_contents(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.title, "Test Category")

    def test_category_return_str(self):
        self.assertEqual(str(self.category), "Test Category")


class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.category = Category.objects.create(
            title="Test Category"
        )

        cls.book = Book.objects.create(
            category=cls.category,
            author="Test Author",
            title="Test Title"
        )

    def test_book_contents(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.title, "Test Title")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.category.title, "Test Category")
        self.assertEqual(self.book.is_new(), True)

    def test_book_return_str(self):
        self.assertEqual(str(self.book), "Test Title")

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
