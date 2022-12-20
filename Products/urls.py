from django.urls import path
from .views import *

urlpatterns = [
    path('', all_products_list, name='all_products'),
    path('<slug:slug>/<int:category_id>/', products_by_category, name='products_by_cat'),
    path('<int:category_id>/<slug:slug>/<int:sub_id>/', products_by_subcategory, name='by_sub'),
    path('<slug:category>/<slug:subcategory>/<int:pk>/<slug:slug>/', products_detail, name='product_detail'),
    path('search/', search, name='search'),
]
