from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    def get_category(self, obj):
        """Метод для отображения категории в админке"""
        return (
            obj.subcategory.category.name
            if obj.subcategory and obj.subcategory.category
            else None
        )

    get_category.short_description = "Категория"

    list_display = ("id", "name", "get_category", "subcategory", "price")
    list_filter = ("subcategory",)
    search_fields = ("name", "slug")
