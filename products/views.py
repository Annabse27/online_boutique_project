from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    """Список всех продуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]  # Доступ для всех пользователей
