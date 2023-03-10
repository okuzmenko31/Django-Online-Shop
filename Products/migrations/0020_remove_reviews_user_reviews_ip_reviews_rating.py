# Generated by Django 4.1.3 on 2022-12-11 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0019_productcategory_title_productsubcategory_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='user',
        ),
        migrations.AddField(
            model_name='reviews',
            name='ip',
            field=models.CharField(blank=True, max_length=20, verbose_name='IP address'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='rating',
            field=models.FloatField(blank=True, default=1, verbose_name='Rating'),
            preserve_default=False,
        ),
    ]
