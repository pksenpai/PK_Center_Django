from django.contrib import admin
from .models import *


@admin.register(Item)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(Rating)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(SellerItem)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(Favorite)
class TaskAdmin(admin.ModelAdmin): ...
