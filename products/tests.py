import pytest
from rest_framework.test import APIClient
from .models import Product
from categories.models import Category, SubCategory


@pytest.mark.django_db
class TestProductAPI:

    def test_list_products(self):
        """Проверка успешного получения списка продуктов"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        subcategory = SubCategory.objects.create(
            name="Smartphones", slug="smartphones", category=category
        )
        Product.objects.create(
            name="iPhone", slug="iphone", price=1000, subcategory=subcategory
        )

        client = APIClient()  # Клиент без авторизации
        response = client.get("/api/products/")
        assert response.status_code == 200  # Доступ разрешен для всех
