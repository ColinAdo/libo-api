from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Progress
from books.models import Book, Category

# Progress tets case
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
        self.assertIsNone(self.progress.finish_date)
        self.assertIsNone(self.progress.remaining_time)
        self.assertEqual(self.progress.is_completed, False)
        self.assertEqual(str(self.progress), f"{self.user.username} Progress")

    def test_progress_methods(self):
        self.progress.set_finish_time()
        self.progress.mark_as_complete()

        self.assertEqual(type(self.progress.remaining_time), int)
        self.assertEqual(self.progress.is_completed, True)
        self.assertNotEqual(self.progress.finish_date, None)
