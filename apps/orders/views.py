from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework.views import APIView
from rest_framework.response import Response

from ast import literal_eval

from .models import Order, OrderItem, Discount
from apps.items.models import Item
from apps.users.models import Address
from .serializers import FinalizePaymentSerializer, ShowPaymentSerializer

class CartView(ListView):
    model = Order
    template_name = 'cart.html'
    
    
class FinalizePaymentView(LoginRequiredMixin, APIView):
    login_url = 'users:login'
    redirect_field_name = 'orders:payment'
    
    def get(self, request):
        cookie = request.COOKIES
        print('='*20, cookie.values())

        if cookie:
            cookie_keys = cookie.keys()
            items = {}
            for c in cookie_keys:
                try:
                    if int(c):
                        
                        cookie_value_str = cookie[c]
                        cookie_value_dict = literal_eval(cookie_value_str)
                        
                        # validate & safe the result of eval
                        if not ShowPaymentSerializer(data=cookie_value_dict).is_valid():
                            return Response({'message': 'invalid data!'}, status=400)
                            
                        items.setdefault(c, {'price': float(cookie_value_dict['price']),
                                             'count': int(cookie_value_dict['count'])})
                        
                        
                except ValueError:
                    pass
            
            if items:
                print('*'*10, items)
                items_obj = Item.objects.filter(id__in=items.keys())
                items_dis = {}
                for item in items_obj:
                    try:
                        print(f'>>>>>>{item}')
                        items_dis.setdefault(item.name, str(item.discount)[-4:].strip())
                    except:
                        print(f"no discount! --> {item}")
                        
                order_discount = ... # coming soon...
                
                
                user_addresses = Address.objects.filter(user=request.user).values_list('address')
                return Response({'items': items, 'addresses': user_addresses, 'items_discount': items_dis})
            else:
                return Response({'message': 'cart is empty!'}, status=422)

        else:
           return Response({'message': 'cart is empty!'}, status=422)
       
       
    def post(self, request):
        cookie = request.COOKIES
        print('='*20, cookie.values())

        if cookie:
            cookie_keys = cookie.keys()
            item_id_lst = []
            for c in cookie_keys:
                try:
                    if int(c):
                        
                        cookie_value_str = cookie[c]
                        cookie_value_dict = literal_eval(cookie_value_str)
                        # validate & safe the result of eval
                        if not ShowPaymentSerializer(data=cookie_value_dict).is_valid():
                            return Response({'message': 'invalid data!'}, status=422)

                        price = cookie_value_dict['price']
                        total_price = 0
                        if cookie_value_dict.get('count', None):
                            for _ in range(cookie_value_dict['count']):
                                total_price += price

                            print('>'*5, 'total_price:', total_price)
                            item_id_lst.append(int(c))
                            # return Response({'message': 'your payment successfully paid!', 'total_price': total_price})

                        return Response({'message': 'cart is empty!'}, status=400)
                    
                except ValueError:
                    pass
            else:
                return Response({'message': 'cart is empty!'}, status=400)
            
            serialized_data = FinalizePaymentSerializer(data=request.data)
            if serialized_data.is_valid():
                items = Item.objects.filter(id__in=item_id_lst)
                data = serialized_data.validated_data
                Order.objects.create(
                    status="Is Paid",
                    receiving_date=data['receiving_date'],
                    item=items,
                    user=request.user,
                    address=data['address'],
                )               
                return Response({'data': data})

        else:
           return Response({'message': 'cart is empty!'}, status=400)

