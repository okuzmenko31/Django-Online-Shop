# Generated by Django 4.1.3 on 2022-12-03 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0009_alter_product_options_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, verbose_name="Ім'я товару в посиланні"),
        ),
    ]
