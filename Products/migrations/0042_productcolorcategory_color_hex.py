# Generated by Django 4.1.3 on 2023-01-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0041_alter_productmemorychoice_memory'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolorcategory',
            name='color_hex',
            field=models.CharField(blank=True, max_length=350, verbose_name='Product HEX color'),
        ),
    ]