from django.shortcuts import render
from Products.models import Product, ProductCategory
from .models import AboutUs, RecommendedProductsPhotos


def home_page(request):
    home_info = AboutUs.objects.all()

    top_sell = Product.objects.all().order_by('?').select_related('main_category', 'subcategory').exclude(
        main_category_id=7).exclude(main_category_id=8).exclude(main_category_id=9)
    top_sell_sec = Product.objects.all().order_by('-id').select_related('main_category', 'subcategory').exclude(
        main_category_id=7).exclude(main_category_id=8).exclude(main_category_id=9)

    bu_apple = Product.objects.filter(main_category__name='Apple б/у').order_by('?')
    bu_apple_sec = Product.objects.filter(main_category__name='Apple б/у').order_by('-id')

    recommend_prod = RecommendedProductsPhotos.objects.all()
    context = {
        'home_info': home_info,
        'recommend_prod': recommend_prod,
        'top_sell': top_sell,
        'top_sell_sec': top_sell_sec,
        'bu_apple': bu_apple,
        'bu_apple_sec': bu_apple_sec,
    }
    return render(request, template_name='HomePage/home_page.html', context=context)
