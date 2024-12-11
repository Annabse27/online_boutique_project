import pytest
from rest_framework.test import APIClient
from products.models import Product
from .models import Cart
from categories.models import Category, SubCategory
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCartAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(
            user=self.user
        )  # Убедиться, что корзина создаётся

    def test_view_cart(self):
        """Тест на просмотр корзины"""
        response = self.client.get("/api/cart/")
        assert response.status_code == 200

    def test_add_to_cart(self):
        """Тест на добавление товара в корзину"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        subcategory = SubCategory.objects.create(
            name="Smartphones", slug="smartphones", category=category
        )
        product = Product.objects.create(
            name="iPhone", slug="iphone", price=1000, subcategory=subcategory
        )

        payload = {"product_id": product.id, "quantity": 2}
        response = self.client.post("/api/cart/", payload)
        assert response.status_code == 200
        assert "message" in response.data  # Проверяем, что в ответе есть сообщение

    def test_clear_cart(self):
        """Тест на очистку корзины"""
        category = Category.objects.create(name="Electronics", slug="electronics")
        subcategory = SubCategory.objects.create(
            name="Smartphones", slug="smartphones", category=category
        )
        product = Product.objects.create(
            name="iPhone", slug="iphone", price=1000, subcategory=subcategory
        )

        # Сначала добавляем товар в корзину
        payload = {"product_id": product.id, "quantity": 2}
        self.client.post("/api/cart/", payload)

        # Очищаем корзину
        response = self.client.delete("/api/cart/")
        assert response.status_code == 200
        assert (
            "message" in response.data
        )  # Проверяем, что в ответе есть сообщение об успешной очистке
