# Generated by Django 4.1.3 on 2023-01-01 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0026_alter_productcolorchoice_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, related_name='colors', to='Products.productcolorchoice', verbose_name='Colors'),
        ),
        migrations.AddField(
            model_name='productcolorchoice',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='Products.product', verbose_name='Товар'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productcolorchoice',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productsubcategory', verbose_name='Category'),
        ),
    ]