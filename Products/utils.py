from django.db.models import Q
from Products.models import Product
from .forms import OrderingChoicesForm
from .models import ProductColorChoice, ProductMemoryChoice, ProductVersionChoice


class SearchMixin:
    """Mixin for getting search queryset"""

    @staticmethod
    def get_search(search):
        """This method has a search parameter which is search query from user"""
        queryset = Product.objects.filter(
            Q(name__icontains=search) | Q(characteristics__icontains=search) | Q(
                info__icontains=search) | Q(status__icontains=search)).select_related('main_category',
                                                                                      'subcategory')
        return queryset


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

        # Checking the sort value and adding the appropriate product sorting.
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
    """
    Mixin for getting related choices of product.
    Mixin returns context with choices.
    """

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
                                                    ).select_related('product__main_category',
                                                                     'product__subcategory')
        version = ProductVersionChoice.objects.filter(subcategory=product.subcategory,
                                                      color=product.product_color,
                                                      memory=product.product_memory,
                                                      is_active=True).select_related('product__main_category',
                                                                                     'product__subcategory')

        context = {
            'color': color,
            'memory': memory,
            'version': version
        }
        return context
