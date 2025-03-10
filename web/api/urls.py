from django.urls import path
from .api import api_v1

app_name = "api"

urlpatterns = [
    path('', api_v1.urls),
]