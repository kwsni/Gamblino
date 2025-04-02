from decimal import Decimal

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

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
        'total_value': inv.total_inv_value(),
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
               'total_value': inv.total_inv_value(),
               'inv': inv} | paged_list_context(request, inv_items, 30)
    return TemplateResponse(request, 'inventory/inventory.html', context)


# Utility 
def paged_list_context(request, objects, paginate_by: int):
    paginator = Paginator(objects, paginate_by)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    elided_page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)
    return {'page_obj': page_obj, 'elided_page_range': elided_page_range}
        