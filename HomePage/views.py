from django.shortcuts import render
from Products.models import Product
from .models import AboutUs, RecommendedProductsPhotos


def home_page(request):
    home_info = AboutUs.objects.all()

    top_sell = Product.objects.all().order_by('?').select_related('main_category', 'subcategory')
    top_sell_sec = Product.objects.all().order_by('-id').select_related('main_category', 'subcategory')

    recommend_prod = RecommendedProductsPhotos.objects.all()
    context = {
        'home_info': home_info,
        'recommend_prod': recommend_prod,
        'top_sell': top_sell,
        'top_sell_sec': top_sell_sec,
    }
    return render(request, template_name='HomePage/home_page.html', context=context)
