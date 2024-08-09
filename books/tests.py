from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Book

import os

# Category test case
class CategoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            title='Test Category'
        )

    def test_category_contents(self):
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(self.category.title, 'Test Category')

    def test_category_return_str(self):
        self.assertEqual(str(self.category), 'Test Category')


# Book test case
class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.category = Category.objects.create(
            title='Test Category'
        )

        cls.book = Book.objects.create(
            category=cls.category,
            author='Test Author',
            title='Test Title'
        )

        cls.test_file = SimpleUploadedFile('book.png', b'file_content', content_type='image/png')

    def test_book_contents(self):
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(self.book.title, 'Test Title')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.category.title, 'Test Category')
        self.assertEqual(self.book.is_new(), True)
        self.assertEqual(str(self.book), 'Test Title')

    def test_book_dir_path(self):
        self.book.cover_image = self.test_file
        self.book.save()

        stored_file = self.book.cover_image.name
        direcyory, filename = os.path.split(stored_file)

        expected_path = f'book/{self.book.author}'

        self.assertEqual(direcyory, expected_path)
        self.assertTrue(filename.startswith('book'))

