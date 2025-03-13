from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from allauth.socialaccount.models import SocialAccount
 

class Case(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(100))
    name = models.CharField(max_length=200, default='')
    image = models.URLField(default='')

    def __str__(self):
        return f'{self.name}: ${self.price}'
    
class Item(models.Model):
    class Rarity(models.TextChoices):
        RARE = 'Rare', _('Rare')
        COVERT = 'Covert', _('Covert')
        CLASSIFIED = 'Classified', _('Classified')
        RESTRICTED = 'Restricted', _('Restricted')
        MIL_SPEC_GRADE = 'Mil-Spec', _('Mil-Spec')

        __empty__ = _('Null')

    name = models.CharField(max_length=128, default='')
    rarity = models.CharField(max_length=16, choices=Rarity, default=Rarity.__empty__)
    image = models.URLField(default='')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} ({self.rarity})'
    
class ItemWear(models.Model):
    class Wear(models.TextChoices):
        FACTORY_NEW = 'Factory New', _('Factory New')
        MINIMAL_WEAR = 'Minimal Wear', _('Minimal Wear')
        FIELD_TESTED = 'Field-Tested', _('Field-Tested')
        WELL_WORN = 'Well-Worn', _('Well-Worn')
        BATTLE_SCARRED = 'Battle-Scarred', _('Battle-Scarred')

        __empty__ = _('Null')

    # Composite pk item and wear?
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    wear = models.CharField(max_length=16, choices=Wear, default=Wear.__empty__)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return f'{self.wear} {self.item.name}: ${self.price}'

    
class Inventory(models.Model):
    uid = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(SocialAccount, on_delete=models.SET_NULL, null=True)
    cash = models.DecimalField(default=Decimal(0), max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.uid}: ${self.cash}'
    
class InvItem(models.Model):
    item = models.ForeignKey(ItemWear, on_delete=models.CASCADE)
    inv = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    opened_on = models.DateTimeField("date opened", default=timezone.now)

    def __str__(self):
        return f'{self.inv.uid}\'s {self.item.wear} {self.item.item.name}: ${self.item.price}'

