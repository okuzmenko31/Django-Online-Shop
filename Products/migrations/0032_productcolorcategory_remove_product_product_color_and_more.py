# Generated by Django 4.1.3 on 2023-01-01 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0031_productcolorchoice_esim_glob_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColorCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=350, verbose_name='Product color')),
            ],
            options={
                'verbose_name': 'Color',
                'verbose_name_plural': 'Colors',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_color',
        ),
        migrations.RemoveField(
            model_name='productcolorchoice',
            name='color_template',
        ),
    ]
