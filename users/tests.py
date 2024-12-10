import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserAPI:

    def test_user_registration(self):
        """Тест успешной регистрации пользователя"""
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = client.post('/api/users/register/', payload, format='json')
        assert response.status_code == 201
        assert 'id' in response.data
        assert 'email' in response.data

    def test_registration_with_existing_email(self):
        """Тест попытки регистрации с существующим email"""
        User.objects.create_user(email='testuser@example.com', password='password123')
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'password': 'newpassword123'
        }
        response = client.post('/api/users/register/', payload, format='json')
        assert response.status_code == 400
        assert 'email' in response.data

    def test_successful_login(self):
        """Тест успешного входа пользователя"""
        User.objects.create_user(email='testuser@example.com', password='password123')
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        response = client.post('/api/users/token/', payload, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_with_invalid_password(self):
        """Тест входа с неверным паролем"""
        User.objects.create_user(email='testuser@example.com', password='password123')
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/api/users/token/', payload, format='json')
        assert response.status_code == 401
        assert 'detail' in response.data

    def test_refresh_token(self):
        """Тест обновления токена"""
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        client = APIClient()
        payload = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        login_response = client.post('/api/users/token/', payload, format='json')
        refresh_token = login_response.data['refresh']

        refresh_payload = {'refresh': refresh_token}
        response = client.post('/api/users/token/refresh/', refresh_payload, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
