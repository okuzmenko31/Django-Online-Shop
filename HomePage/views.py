from django.shortcuts import render
from Products.models import Product, ProductCategory
from .models import AboutUs, RecommendedProductsPhotos


def home_page(request):
    home_info = AboutUs.objects.all()

    top_sell = Product.objects.all().order_by('?').select_related('main_category', 'subcategory').exclude(
        main_category_id=7).exclude(main_category_id=8).exclude(main_category_id=9)
    top_sell_sec = Product.objects.all().order_by('-id').select_related('main_category', 'subcategory').exclude(
        main_category_id=7).exclude(main_category_id=8).exclude(main_category_id=9)

    accessories = Product.objects.filter(main_category_id=8)

    gadgets = Product.objects.filter(main_category_id=7)

    recommend_prod = RecommendedProductsPhotos.objects.all()
    context = {
        'home_info': home_info,
        'recommend_prod': recommend_prod,
        'top_sell': top_sell,
        'top_sell_sec': top_sell_sec,
        'accessories': accessories,
        'gadgets': gadgets,
    }
    return render(request, template_name='HomePage/home_page.html', context=context)
