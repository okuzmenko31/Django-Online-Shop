# Generated by Django 4.1.3 on 2022-12-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0010_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='short_info',
        ),
        migrations.AddField(
            model_name='product',
            name='characteristics',
            field=models.TextField(blank=True, verbose_name='Характеристики товару'),
        ),
    ]
