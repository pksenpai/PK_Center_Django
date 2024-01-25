from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): ...

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin): ...

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin): ...
