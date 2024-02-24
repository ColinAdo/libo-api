from django.test import TestCase

from .models import Category


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
