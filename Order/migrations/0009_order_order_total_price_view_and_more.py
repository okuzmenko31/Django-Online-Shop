# Generated by Django 4.1.3 on 2023-01-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0008_orderitem_item_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total_price_view',
            field=models.CharField(blank=True, max_length=350, verbose_name='Order total price with normal view'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_total_price_view',
            field=models.CharField(blank=True, max_length=350, verbose_name='Item total price with normail view'),
        ),
    ]
