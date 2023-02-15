from django.urls import path
from .views import *

urlpatterns = [
    path('', OrderCreate.as_view(), name='order_creation'),
]
