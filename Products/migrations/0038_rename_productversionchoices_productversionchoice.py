# Generated by Django 4.1.3 on 2023-01-01 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0037_alter_productmemorycategory_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductVersionChoices',
            new_name='ProductVersionChoice',
        ),
    ]
