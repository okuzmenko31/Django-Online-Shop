from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .utils import get_search, ProductsSortMixin, ProductRelatedChoicesMixin
from .forms import ReviewsForms, OrderingChoicesForm
from .models import *


class Search(ListView):
    """View for search"""
    model = Product
    template_name = 'Product/products_list.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = get_search(search_query)
        else:
            queryset = self.queryset
        return queryset


class AllProductsList(ProductsSortMixin, ListView):
    """All products view"""
    model = Product
    template_name = 'Products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12
    queryset = Product.objects.all().select_related('main_category', 'subcategory')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllProductsList, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoicesForm(
            {'form': self.request.session.get('sort')})  # getting sort form with stored value
        return context

    def post(self, *args, **kwargs):
        queryset = self.get_queryset()
        context = self.get_sort_context(self.request, queryset)  # creating context with ProductSortMixin method
        return render(self.request, template_name=self.template_name, context=context)


class ProductsByCategory(ProductsSortMixin, ListView):
    """Products by category view"""
    model = Product
    template_name = 'Products/products_by_category.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsByCategory, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoicesForm(
            {'form': self.request.session.get('sort')})  # getting sort form with stored value
        context['category'] = ProductCategory.objects.get(
            pk=self.kwargs['category_id'], slug=self.kwargs['slug'])  # getting product category
        return context

    def get_queryset(self):
        products = Product.objects.filter(main_category_id=self.kwargs['category_id']).select_related(
            'main_category',
            'subcategory')
        return products

    def post(self, *args, **kwargs):
        queryset = self.get_queryset()

        context = {
            'category': ProductCategory.objects.get(pk=self.kwargs['category_id']),
        }
        context.update(self.get_sort_context(self.request, queryset))
        # adding to the existing context sort form and sorted products

        return render(self.request, template_name=self.template_name, context=context)


class ProductsBySubCategory(ProductsSortMixin, ListView):
    """Products by subcategory view"""
    model = Product
    template_name = 'Products/products_by_subcategory.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsBySubCategory, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoicesForm(
            {'form': self.request.session.get('sort')})
        context['subcategory'] = ProductSubcategory.objects.get(
            pk=self.kwargs['sub_id'])
        return context

    def get_queryset(self):
        products = Product.objects.filter(
            subcategory_id=self.kwargs['sub_id'],
            main_category_id=self.kwargs['category_id']).select_related('main_category', 'subcategory')
        return products

    def post(self, *args, **kwargs):
        queryset = self.get_queryset()

        context = {
            'subcategory': ProductSubcategory.objects.get(pk=self.kwargs['sub_id']),
        }
        context.update(self.get_sort_context(self.request, queryset))
        # adding to the existing context sort form and sorted products

        return render(self.request, template_name=self.template_name, context=context)


class ProductsDetailView(ProductRelatedChoicesMixin, DetailView):
    """Product detail view"""
    model = Product
    template_name = 'Products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Added to the context colors, memory and version choices
         which related with the product. Also added photos and reviews which related
         with the product too, form and recommended products."""
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        context.update(self.get_related_choices(product))
        context['photos'] = ProductPhotos.objects.filter(product=product)
        context['reviews'] = Reviews.objects.filter(product=product)
        context['recommended_products'] = Product.objects.all().order_by('?').select_related('main_category',
                                                                                             'subcategory')
        context['form'] = ReviewsForms()
        return context

    def post(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form = ReviewsForms(self.request.POST)

        if form.is_valid():
            data = Reviews()
            data.name = form.cleaned_data['name']
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            data.ip = self.request.META.get('REMOTE_ADDR')
            data.product = product
            data.save()

            return HttpResponseRedirect(self.request.path)
