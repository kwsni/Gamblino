from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from decimal import Decimal
 
class Case(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(100))
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return f'{self.name}: ${self.price}'
    
class Item(models.Model):
    name = models.CharField(max_length=200, default='')
    rarity = models.CharField(max_length=24, default='')
    wear = models.CharField(max_length=24, default='')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal(0))
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.rarity} {self.wear} {self.name}: ${self.price}'
    
class Player(AbstractUser):
    cash = models.DecimalField(default=Decimal(0), max_digits=15, decimal_places=2)

    def __str__(self):
        return f'{self.username}: ${self.cash}'
    
class PlayerItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    opened_on = models.DateTimeField("date opened", default=timezone.now)

    def __str__(self):
        return f'{self.player.username}\'s {self.item.wear} {self.item.name}: ${self.item.price}'

