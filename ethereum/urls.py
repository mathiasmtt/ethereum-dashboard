from django.urls import path
from .views import register, login_view, address_list, dashboard, home, set_theme
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', home, name='home'),
    path('addresses/', address_list, name='address_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('set_theme/', set_theme, name='set_theme'),
]
