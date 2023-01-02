from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .utils import *
from .forms import ReviewsForms, OrderingChoices
from .models import *


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

    all_sort_form = OrderingChoices(request.POST or {'form': request.session.get('all_sort')})

    """Creating the key of sort in the session and passing the data from the form"""
    if request.method == 'POST':
        if all_sort_form.is_valid():
            request.session['all_sort'] = all_sort_form.cleaned_data['ordering']
    all_sort = request.session.get('all_sort')

    if all_sort == 'standard':
        products = products.order_by('-id')
    elif all_sort == 'cheaper':
        products = products.order_by('price_with_discount')
    elif all_sort == 'expensive':
        products = products.order_by('-price_with_discount')

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 12)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    return render(request, 'Products/products_list.html', {'page_obj': page_objects, 'sort_form': all_sort_form})


def products_by_category(request, category_id, slug):
    """Getting products by their category"""

    category = get_object_or_404(ProductCategory, pk=category_id, slug=slug)  # getting category primary key and slug

    products = Product.objects.filter(
        main_category_id=category_id).select_related('main_category',
                                                     'subcategory')

    cat_sort_form = OrderingChoices(request.POST or {'form': request.session.get('cat_sort')})

    """Creating the key of sort in the session and passing the data from the form"""
    if request.method == 'POST':
        if cat_sort_form.is_valid():
            request.session['cat_sort'] = cat_sort_form.cleaned_data['ordering']
    cat_sort = request.session.get('cat_sort')

    if cat_sort == 'standard':
        products = products.order_by('-id')
    elif cat_sort == 'cheaper':
        products = products.order_by('price_with_discount')
    elif cat_sort == 'expensive':
        products = products.order_by('-price_with_discount')

    # filtering products by category_id which = category primary key

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'category': category,
        'products': products,
        'page_obj': page_objects,
        'sort_form': cat_sort_form
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

    sub_sort_form = OrderingChoices(request.POST or {'form': request.session.get('sub_sort')})

    """Creating the key of sort in the session and passing the data from the form"""
    if request.method == 'POST':
        if sub_sort_form.is_valid():
            request.session['sub_sort'] = sub_sort_form.cleaned_data['ordering']
    sub_sort = request.session.get('sub_sort')

    if sub_sort == 'standards':
        products = products.order_by('-id')
    elif sub_sort == 'cheaper':
        products = products.order_by('price_with_discount')
    elif sub_sort == 'expensive':
        products = products.order_by('-price_with_discount')

    """Passing the received data to the paginator"""

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)

    context = {
        'products': products,
        'page_obj': page_objects,
        'subcategory': subcategory,
        'sort_form': sub_sort_form,
    }
    return render(request, template_name='Products/products_by_subcategory.html', context=context)


def products_detail(request, pk, category, subcategory, slug):
    """Getting product_detail"""

    product = Product.objects.get(pk=pk)  # getting product by primary_key
    product_slug = Product.objects.get(slug=slug)  # getting product slug
    category = ProductCategory.objects.get(slug=category)  # getting category_slug
    subcategory = ProductSubCategory.objects.get(slug=subcategory)  # getting subcategory_slug

    color = ProductColorChoice.objects.filter(category=product.subcategory,
                                              memory=product.product_memory, version=product.product_version,
                                              is_active=True)

    memory = ProductMemoryChoice.objects.filter(category=product.subcategory, color=product.product_color,
                                                version=product.product_version, is_active=True)

    version = ProductVersionChoice.objects.filter(category=product.subcategory, color=product.product_color,
                                                  memory=product.product_memory, is_active=True)

    reviews = Reviews.objects.filter(product=product)  # filtering reviews by product

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
    context = {
        'product': product,
        'form': form,
        'reviews': reviews,
        'color': color,
        'memory': memory,
        'version': version
    }
    return render(request, template_name='Products/product_detail.html', context=context)
