from django.db import models
from categories.models import SubCategory


class Product(models.Model):
    """Модель для продуктов"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(
        SubCategory, related_name="products", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    @property
    def category(self):
        """Возвращает категорию через subcategory"""
        return (
            self.subcategory.category.name
            if self.subcategory and self.subcategory.category
            else None
        )
