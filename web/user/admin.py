from django.contrib import admin

from .models import User, Case, Item

# Register your models here.
admin.site.register(User)
admin.site.register(Case)
admin.site.register(Item)