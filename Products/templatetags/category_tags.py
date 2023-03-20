from django import template
from Products.models import ProductCategory

register = template.Library()


@register.simple_tag()
def get_product_category():
    """Simple tag for getting products categories."""

    return ProductCategory.objects.all().prefetch_related('subcategory__main_category')

