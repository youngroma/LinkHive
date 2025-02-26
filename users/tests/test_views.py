from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_with_referral_code(self):
        # Создаем реферера
        referrer = get_user_model().objects.create_user(
            email='referrer@example.com',
            username='referrer',
            password='password123'
        )
        referral_code = str(referrer.referral_code)

        url = '/api/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123',
            'referral_code': referral_code
        }
        response = self.client.post(url, data, format='json')

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь создан с правильными данными
        user = get_user_model().objects.get(email='newuser@example.com')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.referred_by, referrer)

    def test_register_user_without_referral_code(self):
        url = '/api/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь создан без реферала
        user = get_user_model().objects.get(email='newuser@example.com')
        self.assertIsNone(user.referred_by)

    def test_register_user_with_invalid_referral_code(self):
        url = '/api/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'password123',
            'referral_code': 'invalid-code'  # Недействительный код
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что регистрация не удалась из-за недействительного кода
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Invalid referral code')

    def test_register_user_with_existing_email(self):
        # Создаем первого пользователя
        get_user_model().objects.create_user(
            email='existinguser@example.com',
            username='existinguser',
            password='password123'
        )

        url = '/api/register/'
        data = {
            'email': 'existinguser@example.com',  # Email уже существует
            'username': 'newuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что регистрация не удалась из-за существующего email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Email already in use')


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

    def test_login_success(self):
        url = '/api/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем успешный вход
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.json())

    def test_login_failure_wrong_password(self):
        url = '/api/login/'
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'  # Неправильный пароль
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что вход не удался
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'Invalid credentials')

    def test_login_failure_nonexistent_user(self):
        url = '/api/login/'
        data = {
            'email': 'nonexistent@example.com',  # Пользователя не существует
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')

        # Проверяем, что вход не удался
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()['message'], 'Invalid credentials')