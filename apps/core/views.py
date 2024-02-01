from django.shortcuts import render

from django.views.generic.base import TemplateView

from apps.sellers.models import Seller
from apps.items.models import Item
 

class Home(TemplateView):
    template_name = "home.html"
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Item().top_rated_items()
        print(items)
        context.setdefault("items", items)
    #     top_sellers = Seller.objects.filter(
    #         rank__isnull=False, 
    #         rank__lte=10,
    #     ).order_by('rank')
        
    #     top_items = Item.objects.filter(
            
    #     )
        
    #     context.setdefault("top_sellers", top_sellers)
        context.setdefault("bg_color", "black")
        return render(request, self.template_name, context)
        