from datetime import datetime

import factory.declarations as factory
import factory.faker as faker
from allauth.socialaccount.models import SocialAccount
from factory.django import DjangoModelFactory

from .models import Inventory, InvItem, ItemPrice


class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory
    
    uid = factory.Sequence(lambda n: n)
    user = factory.Iterator(SocialAccount.objects.all())
    cash = faker.Faker('pydecimal', right_digits=2, max_value=9999)

class InvItemFactory(DjangoModelFactory):
    class Meta:
        model = InvItem
    
    item = factory.Iterator(ItemPrice.objects.all())
    inv = factory.SubFactory(InventoryFactory)
    opened_on = factory.LazyFunction(datetime.now)
