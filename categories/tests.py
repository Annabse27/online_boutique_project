import pytest
from rest_framework.test import APIClient
from .models import Category


@pytest.mark.django_db
class TestCategoryAPI:

    def test_list_categories(self):
        client = APIClient()  # Клиент без авторизации
        response = client.get('/api/categories/')
        assert response.status_code == 200  # Доступ разрешен для всех

    def test_list_categories_pagination(self):
        """Проверяем пагинацию для списка категорий"""
        for i in range(15):  # Создаем 15 категорий
            Category.objects.create(name=f'Category {i}', slug=f'category-{i}')

        client = APIClient()
        response = client.get('/api/categories/?page=1')
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) == 10  # Проверяем, что на первой странице 10 категорий
        assert 'next' in response.data  # Убедитесь, что есть ссылка "next"
