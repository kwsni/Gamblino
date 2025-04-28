from decimal import Decimal
from os import getenv

from allauth.socialaccount.models import SocialAccount
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from inventory.models import Case, Inventory, InvItem, Item, ItemPrice
from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from .schemas import LootSchema, PatchCasePriceSchema, PatchItemPriceSchema

load_dotenv()

# Authentication for the Discord bot only
class BotAuth(APIKeyHeader):
    param_name = 'X-API-Key'

    def authenticate(self, request, key):
        if key == getenv('CLIENT_SECRET'):
            return True

api_v1 = NinjaAPI(version='1.0')

@api_v1.post('/open-case', auth=BotAuth())
def case(request, loot: LootSchema):
    inv, inv_created = Inventory.objects.get_or_create(
        uid=loot.uid,
        defaults={
            'uid': loot.uid,
            'cash': Decimal(0)
        }
    )
    if inv.user is None:
        try:
            user = SocialAccount.objects.get(uid=inv.uid)
            inv.user = user
            user.save()
        except SocialAccount.DoesNotExist:
            pass
    item = ItemPrice.objects.get(item__name=loot.item, wear=loot.wear, stattrak=bool(loot.stattrak))
    if isinstance(item, ItemPrice):
        if isinstance(
            InvItem.objects.create(
                inv=inv,
                item=item
            ), InvItem
        ):
            return 201, {'msg': f'Created new inventory for {loot.username}'} if inv_created else 200, {
                    'msg': f'Updated {loot.username}\'s inventory'}
        else:
            return 500, {'msg': 'Server error: Unable to update player inventory'}
    else:
        return 404, {'msg': 'Item does not exist'}

@api_v1.patch('/case/{name}/price')
def update_case_price(request, name: str, payload: PatchCasePriceSchema):
    case = get_object_or_404(Case, name=name)
    for attr, value in payload.dict().items():
        setattr(case, attr, value)
    case.save()
    return 200

@api_v1.patch('/item/{name}/{wear}/price')
def update_item_price(request, name: str, wear: str, payload: PatchItemPriceSchema):
    item = get_object_or_404(Item, name=name)
    itemprice = get_object_or_404(ItemPrice, item=item, wear=wear, stattrak=False)
    for attr, value in payload.dict().items():
        setattr(itemprice, attr, value)
    itemprice.save()
    return 200

@api_v1.patch('/item/{name}/{wear}/stattrak/price')
def update_stattrak_item_price(request, name: str, wear: str, payload: PatchItemPriceSchema):
    item = get_object_or_404(Item, name=name)
    itemprice = get_object_or_404(ItemPrice, item=item, wear=wear, stattrak=True)
    for attr, value in payload.dict().items():
        setattr(itemprice, attr, value)
    itemprice.save()
    return 200