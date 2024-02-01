from django.db import models
from apps.core.models import LogicalBaseModel, StatusMixin, Category
from django.contrib.auth import get_user_model; User = get_user_model()
from apps.sellers.models import Seller

from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.core.cache import cache
from django.utils.functional import cached_property
from ckeditor.fields import RichTextField


class Item(LogicalBaseModel, StatusMixin):
    """\_______________[MAIN]_______________/"""
    name        = models.CharField(max_length=300,verbose_name=_("Name"))
    brand       = models.CharField(max_length=200,verbose_name=_("Brand"))
    description = RichTextField(verbose_name=_("Description"))
    # Total count calculate with sum of every SellerItem counts!

    """\_____________[RELATIONS]_____________/"""
    category = models.ForeignKey(
        to           = Category,
        on_delete    = models.CASCADE,
        verbose_name = _("Category"),
        related_name = 'category_item',
    )

    item_seller = models.ManyToManyField(
        to           = Seller,
        through      = "SellerItem",
        verbose_name = _("Seller"),
        related_name = 'seller_item',
    )

    score = models.ManyToManyField(
        to           = User,
        through      = "Rating",
        verbose_name = _("Score"),
        related_name = 'score_item',
    )
        
    like = models.ManyToManyField(
        to           = User,
        through      = "Favorite",
        verbose_name = _("Like"),
        related_name = 'liked_item',
    )

    class Meta:
        verbose_name_plural = _("Items")
        verbose_name        = _("Item")
        ordering            =  ("?",)
        
    def get_first_image(self):
        if first_image := self.image.first():
            return first_image
        return None
    
    @cached_property
    def cached_average(self):
        cache_key = f"item_avg[{self.pk}]"
        cached_value = cache.get(cache_key)
        if cached_value:
            return cached_value

        average_score = self.rating.aggregate(avg_score=models.Avg('score'))['avg_score']
        rounded_average_score = round(average_score, 1)
        print(rounded_average_score)
        cache.set(cache_key, rounded_average_score, 86400)  # expire every day
        return rounded_average_score
    
    def top_rated_items(self, limit=10):
        cache_key = f"top_rated_items_{limit}"
        cached_items = cache.get(cache_key)
        if cached_items:
            return cached_items

        top_items = Item.objects.annotate(avg_score=models.Avg('rating__score')).order_by('-avg_score')[:limit]
        cache.set(cache_key, top_items, 21600) # expire every 6 hour
        return top_items
    
    def get_absolute_url(self):
        return reverse("items:item_details", args=[self.id])

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    """ high size images for Item & Post media """
    src  = models.ImageField(upload_to='images/item/')
    item = models.ForeignKey(
        to           = Item,
        on_delete    = models.CASCADE,
        verbose_name = _("image item"),
    )


STAR_CHOICES = [
    (0, "0"),
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]

class Rating(models.Model):

    """\_______________[MAIN]_______________/"""
    score = models.IntegerField(
        choices    = STAR_CHOICES,
        # editable   = False,
        validators = [
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )
    
    """\_____________[RELATIONS]_____________/"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    class Meta:
        verbose_name_plural = _("Ratings")
        verbose_name        = _("Rating")

    # def clean(self): # have %%%BUG%%%
    #     super().clean()
    #     if self.__class__.objects.filter(user=self.user, item=self.item).exists():
    #         raise ValidationError("You have already rated this item.")

    def __str__(self):
        return f"{self.score}"
    

class SellerItem(models.Model):
    """\_______________[MAIN]_______________/"""
    price       = models.DecimalField(max_digits=30,decimal_places=2,verbose_name=_("Price"))
    count       = models.PositiveIntegerField()
    orginality  = models.BooleanField(default=False)
    attribute   = RichTextField(verbose_name=_("Attributes"))
    
    """\_____________[RELATIONS]_____________/"""
    item   = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("Item"),   related_name='seller')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name=_("Seller"), related_name='item')

    class Meta:
        verbose_name_plural = _("Seller Items")
        verbose_name        = _("Seller Item")
        ordering            =  ("seller__rank",)
        
    def __str__(self):
        return str(self.seller)
            

class Favorite(models.Model):
    """\_____________[RELATIONS]_____________/"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        verbose_name_plural = _("Favorites")
        verbose_name        = _("Favorite")
        
    def __str__(self):
        return str(user)

