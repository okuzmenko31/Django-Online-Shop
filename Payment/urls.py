from django.urls import path
from .views import *

urlpatterns = [
    path('', PaymentProcess.as_view(), name='payment_process'),
    path('done/', PaymentDone.as_view(), name='payment_done'),
    path('cancel/', PaymentCancel.as_view(), name='payment_cancel'),
]
