from django.test import TestCase
from decimal import Decimal

from shop import models

class ModelsTestCase(TestCase):
    """Test shop models."""

    def test_create_category_success(self):
        """Test create category object is success."""
        name = 'test name'
        slug = 'test slug'
        category = models.Category.objects.create(name=name, slug=slug)
        
        self.assertIsNotNone(category)
        self.assertEqual(category.name, name)
        self.assertEqual(category.slug, slug)

    def test_create_product_success(self):
        """Test create product object is success."""
        category = models.Category.objects.create(name='name', slug='slug')
        expected = {
            'category': category,
            'name': 'name',
            'slug': 'slug',
            'price': Decimal('13.99'),
            'available': False
        }
        product = models.Product.objects.create(**expected)

        self.assertIsNotNone(product)
        for k, v in expected.items():
            self.assertEqual(getattr(product, k), v)