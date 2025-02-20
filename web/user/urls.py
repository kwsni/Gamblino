from django.urls import path

from .views import IndexView, ProfileView, InventoryView

app_name = "user"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<int:pk>/", ProfileView.as_view(), name='profile'),
    path("<int:pk>/inventory/", InventoryView.as_view(), name='inventory'),
]
