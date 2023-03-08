from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('authentication/', Authentication.as_view(), name='authentication')
]
