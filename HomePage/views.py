from django.shortcuts import render
from django.views import View

from Products.models import Product, ProductCategory
from .models import AboutUs, RecommendedProductsPhotos


class HomePage(View):

    def get(self, *args, **kwargs):
        home_info = AboutUs.objects.all()

        top_sell = Product.objects.all().order_by('?').select_related('main_category', 'subcategory').exclude(
            main_category_id=7).exclude(main_category_id=8).exclude(main_category_id=9)

        accessories = Product.objects.filter(main_category_id=8).select_related('main_category', 'subcategory')

        gadgets = Product.objects.filter(main_category_id=7).select_related('main_category', 'subcategory')

        recommend_prod = RecommendedProductsPhotos.objects.all().only('photo')
        context = {
            'home_info': home_info,
            'recommend_prod': recommend_prod,
            'top_sell': top_sell,
            'accessories': accessories,
            'gadgets': gadgets,
        }
        return render(self.request, template_name='HomePage/home_page.html', context=context)
