from django.db.models.signals import post_save
from django.dispatch import receiver
from Products.services import get_price_in_usd, get_discount
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
        if order_bonuses > 0:
            order_bonuses_usd += get_price_in_usd(order_bonuses)

    if instance.order.user:

        if instance.order.use_bonuses:
            """If user want to spend his bonuses and his
            balance is more than the total amount of the order."""
            user_bonuses = instance.order.user.bonuses_balance
            user_bonuses_usd = instance.order.user.bonuses_balance_usd

            if user_bonuses >= order_total_price and user_bonuses_usd >= order_total_price_usd:
                # If user's balance is more than order total price,
                # he won't need to pay with payment method, money
                # will be deducted from his bonuses balance.
                if instance.order.coupon:
                    order_total_price = get_discount(order_total_price, order.coupon.discount)
                    instance.order.coupon.is_active = False
                    instance.order.coupon.save()

                instance.order.user.bonuses_balance = user_bonuses - order_total_price
                instance.order.user.bonuses_balance_usd = user_bonuses_usd - order_total_price_usd
                instance.order.user.save()

                order_total_price = 0

    instance.order.order_total_price = order_total_price

    if order_total_price > 0:
        instance.order.order_total_price_usd = get_price_in_usd(order_total_price)
    else:
        instance.order.order_total_price_usd = 0

    instance.order.order_bonuses = order_bonuses
    instance.order.order_bonuses_usd = get_price_in_usd(order_bonuses)
    instance.order.save(force_update=True)
