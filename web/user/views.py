from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Player, Item, PlayerItem

# Create your views here.

class IndexView(ListView):
    template_name = "user/users.html"
    context_object_name = "user_list"

    def get_queryset(self):
        return Player.objects.order_by("-id")[:10]
    
class ProfileView(DetailView):
    model = Player
    template_name = "user/profile.html"

class InventoryView(ListView):
    paginate_by = 20
    template_name = "user/inventory.html"
    
    def get_queryset(self):
        self.player = get_object_or_404(Player, pk=self.kwargs['pk'])
        self.inventory = PlayerItem.objects.filter(player=self.player)
        return self.inventory
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.player
        context['inventory'] = self.inventory
        return context
        