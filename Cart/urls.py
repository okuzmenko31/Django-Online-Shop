from django.urls import path
from .views import *

urlpatterns = [
    path('', CartDetail.as_view(), name='cart'),
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartRemove.as_view(), name='cart_remove'),
    path('add_quanity/<int:product_id>/', CartAddQuantity.as_view(), name='cart_add_quantity'),
    path('minus_quantity/<int:product_id>/', CartMinusQuantity.as_view(), name='cart_minus_quantity')
]
