from django.shortcuts import render

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Order, OrderItem


class OrderDetails(View):...

class CartView(ListView):
    model = Order
    template_name = 'cart.html'
    
    