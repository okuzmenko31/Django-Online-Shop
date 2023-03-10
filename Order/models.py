from django.db import models
from Products.models import Product
from .services import *
from Products.services import get_price_sep


class Order(models.Model):
    """Model of order"""
    name = models.CharField(max_length=300, verbose_name="Name")
    last_name = models.CharField(max_length=300, verbose_name='Last name')
    surname = models.CharField(max_length=300, verbose_name='Surname', blank=True)
    phone = models.CharField(max_length=200, verbose_name='Phone number', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Order creation date')
    updated = models.DateTimeField(auto_now=True, verbose_name='Order update date')
    email = models.EmailField(verbose_name='Email', blank=True)
    address = models.CharField(max_length=250, verbose_name='Address')
    post_office = models.CharField(max_length=200, verbose_name='Post office', blank=True)
    country = models.CharField(max_length=250, verbose_name='Country', blank=True)
    city = models.CharField(max_length=250, verbose_name='City or town', blank=True)
    paid = models.BooleanField(default=False, verbose_name='Paid')
    order_total_price = models.IntegerField(verbose_name='Order total price', default=0)
    order_total_price_usd = models.IntegerField(verbose_name='Order total price in USD', default=0)

    def __str__(self):
        return f"Order ID: {self.id}, customer name and last name: {self.name} {self.last_name}"

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'Orders'

    def get_order_total_price_view(self):
        order_total_price_view = get_price_sep(self.order_total_price)
        return order_total_price_view

    def get_order_total_price_usd_view(self):
        order_total_price_usd_view = get_price_sep(self.order_total_price_usd)
        return order_total_price_usd_view


class OrderItem(models.Model):
    """Model of orders items"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Order')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Product')
    price = models.IntegerField(verbose_name='Product price')
    price_usd = models.IntegerField(verbose_name='Price per item in dollars', default=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity of product')
    item_total_price = models.IntegerField(verbose_name='Total price of item', default=0)
    item_total_price_usd = models.IntegerField(verbose_name='Total price of item in usd', default=0)

    def __str__(self):
        return f'ID: {self.id}'

    def save(self, *args, **kwargs):
        self.item_total_price = get_product_cost(self.price, self.quantity)
        self.item_total_price_usd = get_product_cost(self.price_usd, self.quantity)
        return super(OrderItem, self).save(*args, **kwargs)

    def get_total_price_view(self):
        item_total_price_view = get_price_sep(self.item_total_price)
        return item_total_price_view

    def get_total_price_usd_view(self):
        item_total_price_usd_view = get_price_sep(self.item_total_price_usd)
        return item_total_price_usd_view
