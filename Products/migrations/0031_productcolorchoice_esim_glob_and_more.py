# Generated by Django 4.1.3 on 2023-01-01 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0030_productesimglobalcategory_remove_product_e_sim_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolorchoice',
            name='esim_glob',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.productesimglobalcategory', verbose_name='Product esim or global'),
        ),
        migrations.AddField(
            model_name='productcolorchoice',
            name='memory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.productmemorycategory', verbose_name='Product memory size'),
        ),
    ]