from django.shortcuts import render
from django.db.models import Q

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

from .models import Item


class ItemsList(ListView):
    model = Item
    template_name = "items_list.html"
    context_object_name = "items"
    paginate_by = 20
    
    def get_queryset(self):
        if searched:= self.request.GET.get("searched"):
            searched: str = searched.strip() # remove extra space's :3
            searched_result: queryset = self.model.objects.filter(
                Q(name__icontains=searched) | Q(description__icontains=searched)
            )
            return searched_result
        else:
            return super().get_queryset().order_by('?')
    

class ItemDetails(DetailView):...
