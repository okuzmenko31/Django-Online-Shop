from django import template
from Products.models import ProductCategory

register = template.Library()


@register.simple_tag()
def get_product_category():
    return ProductCategory.objects.all()

