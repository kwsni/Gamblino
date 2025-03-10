from ninja import NinjaAPI, Schema
from ninja.security import APIKeyHeader
from user.models import Player, PlayerItem, Item
from django.contrib.auth.hashers import make_password
from gamblino.util import secret_keygen
from os import getenv
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

# Authentication for the Discord bot only
class BotAuth(APIKeyHeader):
    param_name = 'X-API-Key'

    def authenticate(self, request, key):
        if key == getenv('CLIENT_SECRET'):
            return True

api_v1 = NinjaAPI(version='1.0', auth=BotAuth())

class LootSchema(Schema):
    uid: int
    username: str
    item: str
    wear: str
    rarity: str


@api_v1.post('/auth')
def auth(request):
    assert isinstance(request.auth, Player)
    return f'Hello, {request.auth}'

@api_v1.post('/open-case')
def case(request, loot: LootSchema):
    # request contains discord data payload in JSON
    # create playeritem with given data
    # return status
    p, p_created = Player.objects.get_or_create(
        pk=loot.uid,
        defaults={
            'id': loot.uid,
            'username': loot.username,
            'password': make_password(secret_keygen()),
            'cash': Decimal(0)
        }
    )
    item = Item.objects.get(name=loot.item, wear=loot.wear)
    if isinstance(item, Item):
        if isinstance(
            PlayerItem.objects.create(
                player=p,
                item=item
            ), PlayerItem
        ):
            return api_v1.create_response(
                request,
                {
                    'msg': f'Added new user {loot.username} and updated their inventory'
                } if p_created
                else {
                    'msg': f'Updated {loot.username}\'s inventory'
                },
                status=201
            )
        else:
            return api_v1.create_response(
                request,
                {'msg': 'Server error: Unable to add to player inventory'},
                status=500
            )
    else:
        return api_v1.create_response(
            request,
            {'msg': 'Item does not exist'},
            status=404
        )
