from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

from .models import User

# Create your views here.

class IndexView(ListView):
    template_name = "user/index.html"
    context_object_name = "user_list"

    def get_queryset(self):
        return User.objects.order_by("-id")[:10]
    
class ProfileView(DetailView):
    model = User
    template_name = "user/user.html"

class InventoryView(DetailView):
    model = User
    template_name = "user/inventory.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inventory"] = User.objects.get(id=self.kwargs["pk"]).items.all()
        return context