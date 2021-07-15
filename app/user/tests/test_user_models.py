from django.test import TestCase

from django.contrib.auth.models import User


def create(**params):
    user = User.objects.create(**params)
    if 'password' in params:
        user.set_password(params['password'])
        user.save()
    return user


class ModelTests(TestCase):

    def test_create_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        payload = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password',
        }
        user = create(**payload)
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user: User = User.objects\
            .create_superuser('admin@test.com', '12345')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
