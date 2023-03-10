# Generated by Django 4.1.3 on 2022-12-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_alter_order_options_alter_order_confirm_call_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AlterField(
            model_name='order',
            name='patronymic',
            field=models.CharField(max_length=300, verbose_name='По-батькові замовника'),
        ),
        migrations.AlterField(
            model_name='order',
            name='real_name',
            field=models.CharField(max_length=300, verbose_name="Ім'я замовника"),
        ),
        migrations.AlterField(
            model_name='order',
            name='surname',
            field=models.CharField(max_length=300, verbose_name='Фамілія замовника'),
        ),
    ]
