from django.db.models import Q
from Products.models import Product
from .services import get_price_in_usd
from .forms import OrderingChoicesForm
from .models import ProductColorChoice, ProductMemoryChoice, ProductVersionChoice


def get_search(search):
    """Method of getting search query."""
    """The search function parameter is the search result we get in the file views.py"""

    return Product.objects.filter(
        Q(name__icontains=search) | Q(characteristics__icontains=search) | Q(
            full_info__icontains=search) | Q(status__icontains=search)).select_related('main_category', 'subcategory')


class ProductsSortMixin:
    """Mixin for sorting products"""

    @staticmethod
    def get_sort_context(request, queryset):
        """Method which returns context with form and sorted products"""
        form = OrderingChoicesForm(request.POST or {'form': request.session.get('sort')})

        if form.is_valid():
            request.session['sort'] = form.cleaned_data['ordering']
        sort = request.session.get('sort')
        products = queryset

        """Checking the sort value and adding the appropriate product sorting"""
        if sort == 'standard':
            products = products.order_by('-id')
        elif sort == 'cheaper':
            products = products.order_by('price_with_discount')
        elif sort == 'expensive':
            products = products.order_by('-price_with_discount')

        context = {
            'sort_form': form,
            'products': products
        }
        return context


class ProductRelatedChoicesMixin:

    @staticmethod
    def get_related_choices(product):
        color = ProductColorChoice.objects.filter(subcategory=product.subcategory,
                                                  memory=product.product_memory,
                                                  version=product.product_version,
                                                  is_active=True
                                                  ).select_related('product__main_category',
                                                                   'product__subcategory')
        memory = ProductMemoryChoice.objects.filter(subcategory=product.subcategory,
                                                    color=product.product_color,
                                                    version=product.product_version,
                                                    is_active=True
                                                    ).order_by('product__product_memory__int_memory_value'
                                                               ).select_related('product__main_category',
                                                                                'product__subcategory')
        version = ProductVersionChoice.objects.filter(subcategory=product.subcategory,
                                                      color=product.product_color,
                                                      memory=product.product_memory,
                                                      is_active=True).order_by('-id').select_related(
            'product__main_category',
            'product__subcategory'
        )

        context = {
            'color': color,
            'memory': memory,
            'version': version
        }
        return context
