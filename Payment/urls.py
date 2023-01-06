from django.urls import path
from .views import *

urlpatterns = [
    path('', payment_process, name='payment_process'),
    path('done/', payment_done, name='payment_done'),
    path('cancel/', payment_cancel, name='payment_cancel'),
]
