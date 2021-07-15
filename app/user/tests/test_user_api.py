from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.tests import utils
from user.serializers import UserSerializer

USERS_URL = reverse('users-list')
USER_DETAIL_NAME = 'users-detail'
ME_URL = reverse('rest_user_details')
REGISTER_URL = reverse('rest_register')
TOKEN_URL = reverse('rest_login')


def create(**params):
    user = User.objects.create(**params)
    if 'password' in params:
        user.set_password(params['password'])
        user.save()
    return user


def create_superuser(**params):
    return User.objects.create_superuser(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """Tests user registration"""
        payload = {
            'username': 'testuser1212',
            'email': 'test2121@test.com',
            'password1': 'asdflkjasdfklasd',
            'password2': 'asdflkjasdfklasd'
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('key', res.data)

    def test_user_exists(self):
        """Tests creating a user that already exists fails"""
        payload = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'asdflkjasdfklasd'
        }
        create(**payload)
        payload = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'asdflkjasdfklasd',
            'password2': 'asdflkjasdfklasd'
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'username': 'testuser',
            'email': 'testshort@test.com',
            'password1': '1234',
            'password2': '1234',
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)        
        user_exists = User.objects.filter(
                email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'username': 'testuser',
            'email': 'testshort@test.com',
            'password': 'password',
        }
        create(**payload)
        res = self.client.post(TOKEN_URL, {
            'username': 'testuser',
            'password': 'password',
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('key', res.data)

    def test_create_token_invalid_credentials(self):
        """Token is not created if invalid credentials are given"""
        payload = {
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'password',
        }
        create(
            email='test@test.com',
            username='Test',
            password='otherpassword',
        )
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exists"""
        payload = {
            'username': 'testuser',
            'email': 'testshort@test.com',
            'password': 'password',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('key', res.data)
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authetication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test regular user actions"""

    def setUp(self):
        self.client = APIClient()
        payload = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'user',
            'email': 'test@test.com',
            'password': 'password',
        }
        self.user = create(**payload)
        utils.AuthUtils.sign_in(self, self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(res.data, serializer.data)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'first_name': 'Test', 'last_name': 'User'}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertEqual(self.user.last_name, payload['last_name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        payload = {
            'username': 'admin',
            'email': 'admin@test.com',
            'password': 'password',
        }
        self.admin_user = create_superuser(**payload)
        self.client = APIClient()
        utils.AuthUtils.sign_in(self, self.admin_user)
        payload = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'password',
        }
        self.user = create(**payload)

    def test_list_users(self):
        """Test creating user with valid payload is successful"""
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('email', res.data['data'][0])
        self.assertEqual(self.user.email, res.data['data'][0]['email'])

    def test_delete_user(self):
        payload = {
            'username': 'test_delete',
            'email': 'test_delete@test.com',
            'password': 'password',
        }
        user_to_delete = create(**payload)
        user_url = reverse(
            USER_DETAIL_NAME,
            kwargs={'pk': user_to_delete.pk}
        )
        res = self.client.delete(user_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(user_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
