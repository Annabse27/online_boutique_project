# Generated by Django 5.1.4 on 2024-12-10 20:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart",
            options={"verbose_name": "Корзина", "verbose_name_plural": "Корзины"},
        ),
        migrations.AlterModelOptions(
            name="cartitem",
            options={
                "verbose_name": "Элемент корзины",
                "verbose_name_plural": "Элементы корзины",
            },
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
