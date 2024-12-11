from django.urls import path
from .views import CartViewSet

cart_viewset = CartViewSet.as_view(
    {"get": "list", "post": "add_to_cart", "delete": "clear_cart"}
)

urlpatterns = [
    path("", cart_viewset, name="cart"),
    path(
        "remove/",
        CartViewSet.as_view({"delete": "remove_from_cart"}),
        name="remove_from_cart",
    ),
]
