from django.db.models.signals import post_save
from django.dispatch import receiver

from Products.services import get_price_in_usd
from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def item_in_order_post_save(**kwargs):
    instance = kwargs['instance']
    order = instance.order
    all_products_in_order = OrderItem.objects.filter(order=order)

    order_total_price = 0
    order_total_price_usd = 0
    order_bonuses = 0
    order_bonuses_usd = 0

    for item in all_products_in_order:
        """Loop through all the objects in the order"""

        order_total_price += item.item_total_price  # adding calculated value
        # how works get_product_cost method you can learn in services.py
        order_total_price_usd += item.item_total_price_usd
        order_bonuses += item.product.bonuses
        order_bonuses_usd = get_price_in_usd(item.product.bonuses)

    instance.order.order_total_price = order_total_price
    instance.order.order_total_price_usd = order_total_price_usd
    instance.order.order_bonuses = order_bonuses
    instance.order.order_bonuses_usd = order_bonuses_usd
    instance.order.save(force_update=True)
