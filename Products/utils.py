from django.db.models import Q

from Products.forms import OrderingChoices
from Products.models import Product
from .services import get_price_in_usd


def get_search(search):
    """Method of getting search query."""
    """The search function parameter is the search result we get in the file views.py"""

    return Product.objects.filter(
        Q(name__icontains=search) | Q(characteristics__icontains=search) | Q(
            full_info__icontains=search) | Q(status__icontains=search)).select_related('main_category', 'subcategory')


def price_usd():
    products = Product.objects.all()
    for product in products:
        product.price_in_usd = get_price_in_usd(product.price_with_discount)
        product.save()
