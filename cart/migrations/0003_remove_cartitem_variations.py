# Generated by Django 5.0.6 on 2024-06-27 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_cart_created_at_remove_cart_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]
