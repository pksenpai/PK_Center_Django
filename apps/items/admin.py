from django.contrib import admin
from .models import *


admin.site.register(ItemImage)
admin.site.register(Rating)
admin.site.register(SellerItem)
admin.site.register(Favorite)

class ItemImageInline(admin.TabularInline):
    model = ItemImage
    readonly_fields = ('id',)
    extra = 1
    

class ItemRatingInline(admin.TabularInline):
    model = Rating
    readonly_fields = ('id',) #  'score', 'user'
    extra = 1
    
    def clean(self):
        super().clean()
        if Rating.objects.filter(user=self.cleaned_data['user'], item=self.cleaned_data['item']).exists():
            raise ValidationError("You have already rated this item.")


class ItemSellerItemInline(admin.TabularInline):
    model = SellerItem
    readonly_fields = ('id',)
    extra = 1


class ItemFavoriteInline(admin.TabularInline):
    model = Favorite
    readonly_fields = ('id', 'user')
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        ItemSellerItemInline,
        ItemImageInline,
        ItemRatingInline,
        ItemFavoriteInline,
    ]

# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin): ...

# @admin.register(ItemImage)
# class ItemImageAdmin(admin.ModelAdmin): ...

# @admin.register(Rating)
# class RatingAdmin(admin.ModelAdmin): ...

# @admin.register(SellerItem)
# class SellerAdmin(admin.ModelAdmin): ...

# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin): ...
