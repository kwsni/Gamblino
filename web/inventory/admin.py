from django.contrib import admin

from .models import Inventory, Case, Item, InvItem

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Case)
admin.site.register(Item)
admin.site.register(InvItem)