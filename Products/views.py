from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .utils import *
from .forms import ReviewsForms, OrderingChoices
from .models import *


class Search(ListView):
    model = Product
    template_name = 'Products/products_list.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = get_search(search_query)
        else:
            queryset = self.queryset
        return queryset


class AllProductsList(ListView):
    model = Product
    template_name = 'Products/products_list.html'
    context_object_name = 'products'
    paginate_by = 12
    queryset = Product.objects.all().select_related('main_category', 'subcategory')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllProductsList, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoices(
            {'form': self.request.session.get('all_sort')})
        return context

    def post(self, *args, **kwargs):
        sort_form = OrderingChoices(
            self.request.POST or {'form': self.request.session.get('all_sort')})
        if sort_form.is_valid():
            self.request.session['all_sort'] = sort_form.cleaned_data['ordering']
        all_sort = self.request.session.get('all_sort')
        products = self.queryset

        if all_sort == 'standard':
            products = products.order_by('-id')
        elif all_sort == 'cheaper':
            products = products.order_by('price_with_discount')
        elif all_sort == 'expensive':
            products = products.order_by('-price_with_discount')

        context = {
            'sort_form': sort_form,
            'products': products,
        }
        print(self.paginate_by)
        return render(self.request, template_name=self.template_name, context=context)


class ProductsByCategory(ListView):
    model = Product
    template_name = 'Products/products_by_category.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsByCategory, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoices(
            {'form': self.request.session.get('all_sort')})
        context['category'] = ProductCategory.objects.get(
            pk=self.kwargs['category_id'], slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        products = Product.objects.filter(main_category_id=self.kwargs['category_id']).select_related(
            'main_category',
            'subcategory')
        return products

    def post(self, *args, **kwargs):
        cat_sort_form = OrderingChoices(
            self.request.POST or {'form': self.request.session.get('all_sort')})
        if cat_sort_form.is_valid():
            self.request.session['all_sort'] = cat_sort_form.cleaned_data['ordering']
        all_sort = self.request.session.get('all_sort')
        products = self.get_queryset()

        if all_sort == 'standard':
            products = products.order_by('-id')
        elif all_sort == 'cheaper':
            products = products.order_by('price_with_discount')
        elif all_sort == 'expensive':
            products = products.order_by('-price_with_discount')

        context = {
            'category': ProductCategory.objects.get(pk=self.kwargs['category_id']),
            'sort_form': cat_sort_form,
            'products': products,
        }
        return render(self.request, template_name=self.template_name, context=context)


class ProductsBySubCategory(ListView):
    model = Product
    template_name = 'Products/products_by_subcategory.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsBySubCategory, self).get_context_data(**kwargs)
        context['sort_form'] = OrderingChoices(
            {'form': self.request.session.get('all_sort')})
        context['subcategory'] = ProductSubCategory.objects.get(
            pk=self.kwargs['sub_id'])
        return context

    def get_queryset(self):
        products = Product.objects.filter(
            subcategory_id=self.kwargs['sub_id'],
            main_category_id=self.kwargs['category_id']).select_related('main_category', 'subcategory')
        return products

    def post(self, *args, **kwargs):
        sub_sort_form = OrderingChoices(
            self.request.POST or {'form': self.request.session.get('all_sort')})
        if sub_sort_form.is_valid():
            self.request.session['all_sort'] = sub_sort_form.cleaned_data['ordering']
        all_sort = self.request.session.get('all_sort')
        products = self.get_queryset()

        if all_sort == 'standard':
            products = products.order_by('-id')
        elif all_sort == 'cheaper':
            products = products.order_by('price_with_discount')
        elif all_sort == 'expensive':
            products = products.order_by('-price_with_discount')

        context = {
            'subcategory': ProductSubCategory.objects.get(pk=self.kwargs['sub_id']),
            'sort_form': sub_sort_form,
            'products': products,
        }
        return render(self.request, template_name=self.template_name, context=context)


class ProductsDetailView(DetailView):
    model = Product
    template_name = 'Products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['color'] = ProductColorChoice.objects.filter(category=product.subcategory,
                                                             memory=product.product_memory,
                                                             version=product.product_version,
                                                             is_active=True
                                                             ).select_related('product__main_category',
                                                                              'product__subcategory')
        context['memory'] = ProductMemoryChoice.objects.filter(category=product.subcategory,
                                                               color=product.product_color,
                                                               version=product.product_version,
                                                               is_active=True
                                                               ).order_by('product__product_memory__int_memory_value'
                                                                          ).select_related('product__main_category',
                                                                                           'product__subcategory')
        context['version'] = ProductVersionChoice.objects.filter(category=product.subcategory,
                                                                 color=product.product_color,
                                                                 memory=product.product_memory,
                                                                 is_active=True).order_by('-id').select_related(
            'product__main_category',
            'product__subcategory'
        )
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
