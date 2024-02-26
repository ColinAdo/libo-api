from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Category, Book, Progress


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


class ProgressTestCase(TestCase):

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

        cls.progress = Progress.objects.create(
            user=cls.user,
            book=cls.book,
        )

    def test_progress_contents(self):
        self.assertEqual(Progress.objects.count(), 1)
        self.assertEqual(self.progress.user, self.user)
        self.assertEqual(self.progress.book, self.book)
        self.assertEqual(self.progress.finish_date, None)
        self.assertEqual(self.progress.is_completed, False)
        self.assertEqual(str(self.progress), f"{self.user.username} Progress")

    def test_progress_methods(self):
        self.progress.set_finish_time()
        self.progress.mark_as_complete()

        self.assertEqual(type(self.progress.remaining_time), int)
        self.assertEqual(self.progress.is_completed, True)
        self.assertNotEqual(self.progress.finish_date, None)
