# Generated by Django 5.0.6 on 2024-06-17 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kebab', '0003_alter_products_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='products',
            options={'ordering': ['-categories', 'product_price']},
        ),
    ]
