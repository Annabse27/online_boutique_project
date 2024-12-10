from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status, permissions


class CartViewSet(viewsets.ViewSet):
    """Вьюсет для работы с корзиной"""

    permission_classes = [permissions.IsAuthenticated]  # Ограничение на доступ только для авторизованных

    def list(self, request):
        """Просмотр содержимого корзины с пагинацией"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Можно поменять значение
        result_page = paginator.paginate_queryset(cart.items.all(), request)
        serializer = CartItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def add_to_cart(self, request):
        """Добавление товара в корзину"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_200_OK)

    def clear_cart(self, request):
        """Очистка корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_200_OK)

    def remove_from_cart(self, request):
        """Удаление товара из корзины"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Товар не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)
