import factory.declarations as factory
import factory.faker as faker
from factory.django import DjangoModelFactory

from allauth.socialaccount.models import SocialAccount
from .models import Inventory, InvItem, ItemPrice

from datetime import datetime

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
