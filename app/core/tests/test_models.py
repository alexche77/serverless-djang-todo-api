from django.test import TestCase

from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@recipe.com'
        password = 'Test12345'
        user = get_user_model().objects\
            .create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@RECIPE.COM'
        user = get_user_model().objects\
            .create_user(email, '12345')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalida_email(self):
        """Test creating user with no email, raises creating error"""
        with self.assertRaises(ValueError):
            get_user_model().objects\
                .create_user(None, '12345')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user: models.User = get_user_model().objects\
            .create_superuser('admin@recipe.com', '12345')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
