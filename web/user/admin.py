from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Player, Case, Item, PlayerItem

# Register your models here.
admin.site.register(Player)
admin.site.register(Case)
admin.site.register(Item)
admin.site.register(PlayerItem)