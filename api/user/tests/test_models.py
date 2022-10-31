from django.test import TestCase
from django.contrib.auth import get_user_model

def create_user(email='test@example.com', first_name='John', last_name='Doe', password='test12345'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)

class ModelsTests(TestCase):
    """
    Tests for the user models.
    """

    def test_create_user_successful(self):
        """Test creating a user is successful."""
        email = 'test@example.com'
        first_name = 'John'
        last_name = 'Doe'
        password = 'testpass123'
        user = create_user(email=email, first_name=first_name, last_name=last_name, password=password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_create_user_without_email(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='')

    def test_create_user_without_first_name(self):
        """Test that creating a user without a first name raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(first_name='')

    def test_create_user_without_last_name(self):
        """Test that creating a user without a last name raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(last_name='')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(email="test@example.com", first_name='John', last_name='Doe', password='testpass123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)