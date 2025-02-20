from django.db import models

# Create your models here.    
class Case(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2)
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return f'{self.name}: ${self.price}'
    
class Item(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2)
    name = models.CharField(max_length=200, default="")
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name}: ${self.price}'
    
class User(models.Model):
    name = models.CharField(max_length=32, default="")
    cash = models.DecimalField(max_digits=15, decimal_places=2)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'{self.name}: ${self.cash}'

