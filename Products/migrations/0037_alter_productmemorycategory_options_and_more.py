# Generated by Django 4.1.3 on 2023-01-01 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0036_alter_productcolorchoice_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productmemorycategory',
            options={'verbose_name': 'Product memory category', 'verbose_name_plural': 'Product memory categories'},
        ),
        migrations.CreateModel(
            name='ProductVersionChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=300, verbose_name='Version of product')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productsubcategory', verbose_name='Category')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productcolorcategory', verbose_name='Product color')),
                ('memory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.productmemorycategory', verbose_name='Product memory')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version_product', to='Products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Version choice',
                'verbose_name_plural': 'Version choices',
            },
        ),
    ]
