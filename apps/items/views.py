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
    # queryset = Item.objects.prefetch_related('images')
    # print(queryset)

    # def get_queryset(self):
    #     if searched := self.request.GET.get("searched"):
    #         searched: str = searched.strip() # remove extra space's :3
    #         result: queryset = self.model.objects.filter(
    #             Q(name__icontains=searched) | Q(description__icontains=searched)
    #         ).order_by('?')
            
    #     if category := self.request.GET.get("category"):
    #         result: queryset = self.model.objects.filter(category=category).order_by('?')
            
            
    #         return result
    #     else:
    #         return super().get_queryset().order_by('?')
    

# from rest_framework.generics import ListAPIView
# from .models import Item
# from .serializers import ItemSerializer

# class ItemsListView(ListAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer

# class AddToCartView():...

class ItemDetailsView(DetailView):
    model = Item
    template_name = "item_details.html"
    context_object_name = "item"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        
        total_stock = item.seller.aggregate(total_count=Sum('count'))['total_count']
        context['total_stock'] = total_stock
        
        # seller.aggregate(p_sum=Sum('price'))['p_sum']
        
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Item), object_id=item.id)
        context['comments'] = comments
        return context

        # super().clean()
        # if self.__class__.objects.filter(user=self.user, item=self.item).exists():
        #     raise ValidationError("You have already rated this item.")
        
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)
    

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

        
# class CategoryDetailView(DetailView):
#     model = Category
#     template_name = 'category.html'
#     context_object_name = 'categories'

#     def get_context_data(self, kwargs):
#         context = super().get_context_data(kwargs)
#         category = self.get_object()
#         print(category, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         subcategory = Category.objects.filter(replay_cat=category)
#         print(subcategory,'bbbbbbbbbbbbbbbbbbbbbbbbbbbb')
#         if subcategory.exists():
#             products = Product.objects.filter(category__in=subcategory)
#             # context['subcategory'] = subcategory
#             print(products, 'cccccccccccccccccccccccccccccccccccccccccc')
#         else:
#             products = Product.objects.filter(category=category)
#             print(products, 'dddddddddddddddddddddddddddddddddddddddddddd')
#         context['products'] = products
#         print(context, 'e' * 100)
#         return context

# class CategoryListView(ListView):
#     model = Category
#     template_name = "base.html"
#     context_object_name = "categories"
    
