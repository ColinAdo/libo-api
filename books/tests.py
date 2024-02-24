from django.test import TestCase

from .models import Category, Book


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
