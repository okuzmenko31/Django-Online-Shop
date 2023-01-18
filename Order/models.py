from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from Products.models import Product
from .services import *
from Products.services import get_price_sep


class Order(models.Model):
    """Model of order"""
    name = models.CharField(max_length=300, verbose_name="Ім'я")
    last_name = models.CharField(max_length=300, verbose_name='Фамілія')
    phone = models.CharField(max_length=200, verbose_name='Номер телефону', blank=True)
    confirm_call = models.BooleanField(default=False, verbose_name='Дзвінок для підтвердження')
    is_active = models.BooleanField(default=False, verbose_name='Замовлення підтверджено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
    email = models.EmailField(verbose_name='Пошта', blank=True)
    address = models.CharField(max_length=250, verbose_name='Адреса')
    postal_code = models.CharField(max_length=20, verbose_name='Поштовий код')
    city = models.CharField(max_length=100, verbose_name='Місто')
    paid = models.BooleanField(default=False, verbose_name='Замовлення сплачено?')
    order_total_price = models.IntegerField(verbose_name='Order total price', default=0)
    order_total_price_view = models.CharField(max_length=350, verbose_name='Order total price with normal view',
                                              blank=True)
    order_total_price_usd = models.IntegerField(verbose_name='Order total price in USD', default=0)
    order_total_price_usd_view = models.CharField(max_length=350,
                                                  verbose_name='Order total price in usd with normal view',
                                                  blank=True)

    def __str__(self):
        return f"ID замовлення: {self.id}, Ім'я та фамілія замовника: {self.name} {self.last_name}"

    class Meta:
        verbose_name = 'замовлення'
        verbose_name_plural = 'Замовлення'

    def save(self, *args, **kwargs):
        self.order_total_price_view = get_price_sep(self.order_total_price)
        self.order_total_price_usd_view = get_price_sep(self.order_total_price_usd)
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    """Model of item in order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Замовлення')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Ціна товару')
    price_usd = models.IntegerField(verbose_name='Price per item in dollars', default=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name='кількість товару')
    item_total_price = models.IntegerField(verbose_name='Total price of item', default=0)
    item_total_price_usd = models.IntegerField(verbose_name='Total price of item in usd', default=0)

    def __str__(self):
        return f'ID: {self.id}'

    def save(self, *args, **kwargs):
        self.item_total_price = get_product_cost(self.price, self.quantity)
        self.item_total_price_usd = get_product_cost(self.price_usd, self.quantity)
        super(OrderItem, self).save(*args, **kwargs)

    def get_total_price_view(self):
        item_total_price_view = get_price_sep(self.item_total_price)
        return item_total_price_view

    def get_total_price_usd_view(self):
        item_total_price_usd_view = get_price_sep(self.item_total_price_usd)
        return item_total_price_usd_view


def item_in_order_post_save(sender, instance, created, **kwargs):
    """Here we are counting the total_price of order"""
    order = instance.order
    all_products_in_order = OrderItem.objects.filter(order=order)

    order_total_price = 0
    order_total_price_usd = 0

    for item in all_products_in_order:
        """Loop through all the objects in the order"""

        order_total_price += item.item_total_price  # adding calculated value
        # how works get_product_cost method you can learn in services.py
        order_total_price_usd += item.item_total_price_usd

    instance.order.order_total_price = order_total_price
    instance.order.order_total_price_usd = order_total_price_usd
    instance.order.save(force_update=True)


post_save.connect(item_in_order_post_save, sender=OrderItem)
