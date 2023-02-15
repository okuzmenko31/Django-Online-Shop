from django.urls import path
from .views import *

urlpatterns = [
    path('', AllProductsList.as_view(), name='all_products'),
    path('<slug:slug>/<int:category_id>/', ProductsByCategory.as_view(), name='products_by_cat'),
    path('<int:category_id>/<slug:slug>/<int:sub_id>/', ProductsBySubCategory.as_view(), name='by_sub'),
    path('<slug:category>/<slug:subcategory>/<int:pk>/<slug:slug>/', ProductsDetailView.as_view(),
         name='product_detail'),
    path('search/', Search.as_view(), name='search'),
]
