# Generated by Django 4.2.5 on 2024-06-03 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_cart_remove_delivery_delivery_person_order_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(),
        ),
    ]
