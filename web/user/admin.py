from django.contrib import admin

from .models import Player, Case, Item

# Register your models here.
admin.site.register(Player)
admin.site.register(Case)
admin.site.register(Item)