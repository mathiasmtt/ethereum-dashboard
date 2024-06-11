# ethereum/urls.py

from django.urls import path
from .views import address_list, dashboard

urlpatterns = [
    path('', address_list, name='address_list'),
    path('dashboard/', dashboard, name='dashboard'),
]
