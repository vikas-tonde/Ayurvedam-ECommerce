# Generated by Django 4.2.1 on 2023-06-29 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_quantity_alter_cart_id_alter_customer_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
