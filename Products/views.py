from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .utils import *
from .forms import ReviewsForms

from .models import Product, ProductCategory, ProductSubCategory, Reviews


def search(request):
    """Function of rendering search_query"""

    search_query = request.GET.get('search', '')  # getting search query

    if search_query:
        """If we have search_query, we pass the search data to the paginator"""

        products = get_search(search_query)

        paginator = Paginator(products, 12)
        page_num = request.GET.get('page', 1)
        page_objects = paginator.get_page(page_num)
    else:
        """If we dont have search_query, we are getting all products in database and pass data to the paginator"""

        products = Product.objects.all().select_related('main_category', 'subcategory')

        paginator = Paginator(products, 12)
        page_num = request.GET.get('page', 1)
        page_objects = paginator.get_page(page_num)

    return render(request, 'Products/products_list.html', {'page_obj': page_objects})


def all_products_list(request):
    """Getting all products in database"""

    products = Product.objects.all().select_related('main_category', 'subcategory')

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 12)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'Products/products_list.html', {'page_obj': page_objects})


def products_by_category(request, category_id, slug):
    """Getting products by their category"""

    category = get_object_or_404(ProductCategory, pk=category_id, slug=slug)  # getting category primary key and slug

    products = Product.objects.filter(
        main_category_id=category_id).select_related('main_category',
                                                     'subcategory')
    # filtering products by category_id which = category primary key

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'category': category,
        'products': products,
        'page_obj': page_objects,
    }
    return render(request, template_name='Products/products_by_category.html', context=context)


def products_by_subcategory(request, category_id, slug, sub_id):
    """Getting products by subcategory"""

    category = ProductCategory.objects.get(pk=category_id)  # getting category primary key

    subcategory = ProductSubCategory.objects.get(pk=sub_id)  # getting subcategory primary key
    subcategory_slug = ProductSubCategory.objects.get(slug=slug)  # getting subcategory slug

    products = Product.objects.filter(
        subcategory_id=sub_id,
        main_category_id=category_id).select_related('main_category',
                                                     'subcategory')  # filtering by sub_id which = subcategory_id

    # and category_id which = main_category_id

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'products': products,
        'page_obj': page_objects,
        'subcategory': subcategory,
    }
    return render(request, template_name='Products/products_by_subcategory.html', context=context)


def products_detail(request, pk, category, subcategory, slug):
    """Getting product_detail"""

    product = Product.objects.get(pk=pk)  # getting product by primary_key
    product_slug = Product.objects.get(slug=slug)  # getting product slug
    category = ProductCategory.objects.get(slug=category)  # getting category_slug
    subcategory = ProductSubCategory.objects.get(slug=subcategory)  # getting subcategory_slug

    reviews = Reviews.objects.filter(product_id=pk)  # filtering reviews by product primary key

    """Posting reviews and getting them"""

    if request.method == 'POST':
        form = ReviewsForms(request.POST)
        if form.is_valid():
            data = Reviews()
            data.name = form.cleaned_data['name']
            data.review = form.cleaned_data['review']
            data.rating = form.cleaned_data['rating']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product = product
            data.save()

            return HttpResponseRedirect(request.path)  # refresh the page to clear the form
    else:
        form = ReviewsForms()  # form output without data
    return render(request, 'Products/product_detail.html',
                  {'product': product, 'form': form, 'reviews': reviews})
