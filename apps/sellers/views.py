from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Seller


class SellerProfileView(DetailView):
    model = Seller
    template_name = "seller_profile.html"
    context_object_name = "item"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Item), object_id=item.id)
        context['comments'] = comments
        return context
