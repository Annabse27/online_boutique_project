import pytest
from rest_framework.test import APIClient
from .models import Category


@pytest.mark.django_db
class TestCategoryAPI:

    def test_list_categories(self):
        client = APIClient()  # Клиент без авторизации
        response = client.get('/api/categories/')
        assert response.status_code == 200  # Доступ разрешен для всех
