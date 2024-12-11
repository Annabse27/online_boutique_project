from rest_framework.permissions import IsAuthenticated  # Подключить
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from products.models import Product


class CartViewSet(viewsets.ViewSet):
    """Вьюсет для работы с корзиной"""

    permission_classes = [
        IsAuthenticated
    ]  # Доступ только для авторизованных пользователей

    @swagger_auto_schema(
        responses={200: CartSerializer},
    )
    def list(self, request):
        """Просмотр содержимого корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID товара"
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Количество товара (по умолчанию 1)",
                ),
            },
            required=["product_id"],
        ),
        responses={200: openapi.Response("Товар добавлен в корзину")},
    )
    @action(methods=["post"], detail=False)
    def add_to_cart(self, request):
        """Добавление товара в корзину"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            # Устанавливаем начальное количество для нового товара
            cart_item.quantity = int(quantity)
        else:
            # Увеличиваем количество для существующего товара
            cart_item.quantity += int(quantity)

        cart_item.save()

        return Response(
            {"message": "Товар добавлен в корзину"}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={200: openapi.Response("Корзина очищена")})
    @action(methods=["delete"], detail=False)
    def clear_cart(self, request):
        """Очистка корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({"message": "Корзина очищена"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "product_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID товара"
                ),
                "quantity": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Количество товара для удаления (по умолчанию 1)",
                ),
            },
            required=["product_id"],
        ),
        responses={
            200: openapi.Response("Товар успешно удалён или количество уменьшено"),
            404: openapi.Response("Товар не найден в корзине"),
        },
    )
    @action(methods=["delete"], detail=False, url_path="remove")
    def remove_from_cart(self, request):
        """Удаление товара из корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product_id")
        quantity = int(
            request.data.get("quantity", 1)
        )  # Удаляемое количество товара (по умолчанию 1)

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND
            )

        if cart_item.quantity > quantity:
            # Уменьшаем количество, если в корзине больше, чем нужно удалить
            cart_item.quantity -= quantity
            cart_item.save()
            return Response(
                {
                    "message": f"Количество товара уменьшено на {quantity}. Осталось: {cart_item.quantity}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            # Удаляем товар, если его количество меньше или равно запрашиваемому
            cart_item.delete()
            return Response(
                {"message": "Товар полностью удалён из корзины"},
                status=status.HTTP_200_OK,
            )
