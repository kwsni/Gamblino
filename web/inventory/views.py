from decimal import Decimal
from typing import Any
from webbrowser import get

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialAccount

from .models import Inventory, InvItem

# Create your views here.
def index_view(request):
    users = SocialAccount.objects.all()
    context = {} | paged_list_context(request, users, 10)
    return TemplateResponse(request, 'inventory/users.html', context)

def profile_view(request, uid: int):
    socialuser = get_object_or_404(SocialAccount, uid=uid)
    inv, inv_created = Inventory.objects.get_or_create(
        uid=uid,
        defaults={
            'uid': uid,
            'cash': Decimal(0),
            'user': socialuser
        }
    )
    context = {
        'socialuser': socialuser,
        'user_profile': get_object_or_404(User, id=socialuser.user.id),
        'inv': inv
    }
    return TemplateResponse(request, 'inventory/profile.html', context)

def profile_redirect_view(request):
    socialuser = get_object_or_404(SocialAccount, user=request.user)
    return HttpResponseRedirect(f'/user/{socialuser.uid}', status=301)

def inventory_view(request, uid: int):
    socialuser = get_object_or_404(SocialAccount, uid=uid)
    user = get_object_or_404(User, id=socialuser.user.id)
    inv, inv_created = Inventory.objects.get_or_create(
        uid=uid,
        defaults={
            'uid': uid,
            'cash': Decimal(0),
            'user': user
        }
    )
    inv_items = InvItem.objects.filter(inv=inv)
    context = {'socialuser': socialuser,
               'user_profile': user,
               'inv': inv} | paged_list_context(request, inv_items, 10)
    return TemplateResponse(request, 'inventory/inventory.html', context)


# Utility 
def paged_list_context(request, objects, paginate_by: int):
    paginator = Paginator(objects, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {'page_obj': page_obj}
        