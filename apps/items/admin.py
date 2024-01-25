from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin): ...

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin): ...

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin): ...

@admin.register(SellerItem)
class SellerAdmin(admin.ModelAdmin): ...

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin): ...
