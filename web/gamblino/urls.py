from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from allauth.account.views import login, logout, signup
from allauth.socialaccount.providers.discord.views import oauth2_login, oauth2_callback

from api.api import api_v1

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('user/', include('inventory.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/discord/login/', oauth2_login, name='discord_login'),
    path('accounts/discord/login/callback/', oauth2_callback, name='discord_callback'),
    path('accounts/logout/', logout, name='account_logout'),
    path('api/v1/', api_v1.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
