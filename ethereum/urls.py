from django.urls import path
from .views import register, login_view, address_list, dashboard, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),
    path('addresses/', address_list, name='address_list'),
    path('dashboard/', dashboard, name='dashboard'),
]
