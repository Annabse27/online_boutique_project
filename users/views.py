from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    """Получение токена по email и паролю"""
    pass
