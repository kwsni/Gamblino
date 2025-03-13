from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.api import api_v1

urlpatterns = [
    path('', TemplateView.as_view(template_name="homepage.html"), name='index'),
    path('user/', include('inventory.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/', api_v1.urls),
]
