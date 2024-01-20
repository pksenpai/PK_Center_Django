from django.contrib import admin
from .models import *


@admin.register(Order)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(OrderItem)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(Discount)
class TaskAdmin(admin.ModelAdmin): ...
