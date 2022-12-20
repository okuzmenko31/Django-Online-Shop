from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add_quanity/<int:product_id>/', cart_add_quantity, name='cart_add_quantity'),
    path('minus_quantity/<int:product_id>/', cart_minus_quantity, name='cart_minus_quantity')
]
