from django import template
from Products.models import ProductCategory, ProductSubCategory

register = template.Library()


@register.inclusion_tag('Products/_navbar.html')
def get_product_category():
    categories = ProductCategory.objects.all()
    return {'categories': categories}
