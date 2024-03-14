from django.shortcuts import render
from django.db.models import Q, Sum

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

from django.contrib.contenttypes.models import ContentType
from apps.core.models import Comment, Category
from apps.sellers.models import Seller
from .models import Item


class ItemsListView(ListView):
    model = Item
    template_name = "items_list.html"
    context_object_name = "items"
    paginate_by = 2


class ItemDetailsView(DetailView):
    model = Item
    template_name = "item_details.html"
    context_object_name = "item"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        
        total_stock = item.seller.aggregate(total_count=Sum('count'))['total_count']
        context['total_stock'] = total_stock
        
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Item), object_id=item.id)
        context['comments'] = comments
        return context

    
class CategoryDetailView(DetailView):
    model = Category
    template_name = "category.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        items = Item.objects.filter(category=category)
        context['items'] = items
        return context


class SellerDetailView(DetailView):
    model = Seller
    template_name = "seller.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.get_object()
        items = Item.objects.filter(item_seller=seller)
        context['items'] = items
        return context

    
