from allauth.account.views import logout
from allauth.socialaccount.providers.discord.views import oauth2_callback, oauth2_login
from api.api import api_v1
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    path('user/', include('inventory.urls')),
    path('pit-boss/doc/', include('django.contrib.admindocs.urls')),
    path('pit-boss/', admin.site.urls),
    path('accounts/discord/login/', oauth2_login, name='discord_login'),
    path('accounts/discord/login/callback/', oauth2_callback, name='discord_callback'),
    path('accounts/logout/', logout, name='account_logout'),
    path('api/v1/', api_v1.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
