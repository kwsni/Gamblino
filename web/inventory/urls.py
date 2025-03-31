from django.urls import path

from .views import index_view, profile_view, inventory_view, profile_redirect_view

app_name = 'inventory'
urlpatterns = [
    path('', index_view, name='index'),
    path('<int:uid>/', profile_view, name='profile'),
    path('<int:uid>/inventory', inventory_view, name='inventory'),
    path('profile', profile_redirect_view, name='profile_redirect')
]
