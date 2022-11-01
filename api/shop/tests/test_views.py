from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from decimal import Decimal

from shop import models, serializers

CATEGORIES_URL = reverse('shop:category-list')
PRODUCTS_URL = reverse('shop:product-list')

def detail_url(category_slug=None, product_slug=None):
    """Create and return a detail url for a product or category."""
    if product_slug is None and category_slug is not None:
        return reverse('shop:category-detail', args=[category_slug])
    elif product_slug is not None and category_slug is None:
        return reverse('shop:product-detail', args=[product_slug])
    return None

def create_category(name='shirts', slug=None):
    """Create a category."""
    if slug is None:
        slug = name
    category = models.Category.objects.create(name=name, slug=slug)
    return category

def create_product(category, **params):
    default = {
        'category': category,
        'name': 'Super shirt',
        'slug': 'super-shirt',
        'price': Decimal('13.99'),
        'available': True,
    }
    default.update(params)

    product = models.Product.objects.create(**default)
    return product

class PublicShopApiTests(TestCase):
    """
    Test unauthenticated API requests.
    """

    def setUp(self):
        self.client = APIClient()

    def test_get_category_list(self):
        """Test retrieving a list of categories."""
        create_category(name='shirts')
        create_category(name='pants')

        response = self.client.get(CATEGORIES_URL)
        
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_product_list(self):
        """Test retrieving a list of products."""
        category = create_category(name='shirts')
        create_product(category=category)

        response = self.client.get(PRODUCTS_URL)

        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_category_detail(self):
        """Test retrieving a single category."""
        category = create_category(name='shirts')
        
        response = self.client.get(detail_url(category_slug=category.slug))
        serializer = serializers.CategorySerializer(category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_get_product_detail(self):
        """Test retrieving a single product."""
        category = create_category(name='shirts')
        product = create_product(category=category)
        
        response = self.client.get(detail_url(product_slug=product.slug))
        serializer = serializers.ProductDetailSerializer(product)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_category_unauthorized(self):
        """Test POST method in category is not allowed for unauthenticated."""
        response = self.client.post(CATEGORIES_URL, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_product_unauthorized(self):
        """Test POST method in product is not allowed for unauthenticated."""
        response = self.client.post(PRODUCTS_URL, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_or_delete_category_unauthorized(self):
        """Test PUT, PATCH, DELETE methods in category is not allowed for unauthenticated."""
        category = create_category(name='shirts')
        response = self.client.put(detail_url(category_slug=category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(detail_url(category_slug=category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        reponse = self.client.delete(detail_url(category_slug=category.slug))
        self.assertEqual(reponse.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_or_delete_product_unauthorized(self):
        """Test PUT, PATCH, DELETE methods in product is not allowed for unauthenticated."""
        category = create_category(name='shirts')
        product = create_product(category=category)
        response = self.client.put(detail_url(product_slug=product.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(detail_url(product_slug=product.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        reponse = self.client.delete(detail_url(product_slug=product.slug))
        self.assertEqual(reponse.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthenticatedShopApiTests(TestCase):
    """
    Test authenticated API requests.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='user@example.com', first_name='John', last_name='Doe', password='test12345')
        self.client.force_authenticate(self.user)

    def test_post_category_non_staff(self):
        """Test POST method in category is not allowed for non staff users."""
        response = self.client.post(CATEGORIES_URL, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_product_non_staff(self):
        """Test POST method in product is not allowed for non staff users."""
        response = self.client.post(PRODUCTS_URL, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_or_delete_category_non_staff(self):
        """Test PUT, PATCH, DELETE methods in category is not allowed for non staff users."""
        category = create_category(name='shirts')
        response = self.client.put(detail_url(category_slug=category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(detail_url(category_slug=category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        reponse = self.client.delete(detail_url(category_slug=category.slug))
        self.assertEqual(reponse.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_or_delete_product_non_staff(self):
        """Test PUT, PATCH, DELETE methods in product is not allowed for non staff users."""
        category = create_category(name='shirts')
        product = create_product(category=category)
        response = self.client.put(detail_url(product_slug=product.slug), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.patch(detail_url(product_slug=product.slug), {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        reponse = self.client.delete(detail_url(product_slug=product.slug))
        self.assertEqual(reponse.status_code, status.HTTP_403_FORBIDDEN)

class StaffShopApiTests(TestCase):
    """
    Test staff API requests.
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(email='admin@example.com', first_name='John', last_name='Doe', password='test12345')
        self.client.force_authenticate(self.admin)

    def test_post_category_staff(self):
        """Test POST method in category is not allowed for staff users."""
        payload = {
        'name': 'shirts',
        'slug': 'shirts',
        }

        response = self.client.post(CATEGORIES_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = models.Category.objects.get(slug=payload['slug'])
        self.assertIsNotNone(category)
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)

    def test_post_product_staff(self):
        """Test POST method in product is not allowed for staff users."""
        payload = {
        'category': {
            'name': 'shirts',
            'slug': 'shirts'
        },
        'name': 'Super shirt',
        'slug': 'super-shirt',
        'price': Decimal('13.99'),
        'available': True,
        }

        response = self.client.post(PRODUCTS_URL, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = models.Product.objects.get(slug=response.data['slug'])
        self.assertIsNotNone(product)
        category = models.Category.objects.get(slug=payload['category']['slug'])
        for k, v in payload.items():
            if k == 'category':
                self.assertEqual(getattr(product, k), category)
            else:
                self.assertEqual(getattr(product, k), v)

    def test_update_or_delete_category_staff(self):
        """Test PUT, PATCH, DELETE methods in category is not allowed for staff users."""
        category = create_category(name='shirts')
        payload = {
            'name': 'pants',
            'slug': 'pants',
        }

        response = self.client.put(detail_url(category_slug=category.slug), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertIsNotNone(category)
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)

        reponse = self.client.delete(detail_url(category_slug=category.slug))
        self.assertEqual(reponse.status_code, status.HTTP_204_NO_CONTENT)
        exists = models.Category.objects.filter(slug=category.slug).exists()
        self.assertFalse(exists)

    def test_update_or_delete_product_staff(self):
        """Test PUT, PATCH, DELETE methods in product is not allowed for staff users."""
        category = create_category(name='shirts')
        payload = {
        'category': {
            'name': 'pants',
            'slug': 'pants',
        },
        'name': 'Super pants',
        'slug': 'super-pants',
        'price': Decimal('16.99'),
        'available': False,
        }
        product = create_product(category=category)

        response = self.client.put(detail_url(product_slug=product.slug), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertIsNotNone(product)
        category = models.Category.objects.get(slug=payload['category']['slug'])
        for k, v in payload.items():
            if k == 'category':
                self.assertEqual(getattr(product, k), category)
            else:
                self.assertEqual(getattr(product, k), v)

        reponse = self.client.delete(detail_url(product_slug=product.slug))
        self.assertEqual(reponse.status_code, status.HTTP_204_NO_CONTENT)
        exists = models.Product.objects.filter(slug=product.slug).exists()
        self.assertFalse(exists)