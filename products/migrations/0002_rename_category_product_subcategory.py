# Generated by Django 5.1.4 on 2024-12-10 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="category",
            new_name="subcategory",
        ),
    ]
