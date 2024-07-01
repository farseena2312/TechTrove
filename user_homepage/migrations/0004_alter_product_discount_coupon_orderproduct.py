# Generated by Django 5.0.6 on 2024-06-24 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_homepage', '0003_alter_product_discount_coupon_useraddress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_coupon',
            field=models.CharField(default='71A9A2C5', max_length=50),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(max_length=100)),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_homepage.product')),
            ],
        ),
    ]
