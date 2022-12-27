from django.urls import path
from .views import *

urlpatterns = [
    path('', order_create, name='order_creation'),
    path('payment_complete/', process_order, name='payment_complete'),
]
