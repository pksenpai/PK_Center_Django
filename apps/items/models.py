from django.db import models
from apps.core.models import ItemImageBaseModel, StatusMixin, Category
from django.contrib.auth import get_user_model; User = get_user_model()
from apps.sellers.models import Seller

from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.core.cache import cache
from django.utils.functional import cached_property


class Item(ItemImageBaseModel, StatusMixin):
    name        = models.CharField(max_length=300,verbose_name=_("Name"))
    brand       = models.CharField(max_length=200,verbose_name=_("Brand"))
    description = models.TextField(verbose_name=_("Description"))
    price       = models.DecimalField(max_digits=30,decimal_places=2,verbose_name=_("Price"))

    # Total count calculate with sum of every SellerItem counts!

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

    def get_absolute_url(self):
        return reverse("items:item_details", args=[self.id])

    def __str__(self):
        return self.name


class Rating(models.Model):
    class StarChoices(models.TextChoices):
        ZERO_STAR  = 0, _("0")
        ONE_STAR   = 1, _("1")
        TWO_STAR   = 2, _("2")
        THREE_STAR = 3, _("3")
        FOUR_STAR  = 4, _("4")
        FIVE_STAR  = 5, _("5")

    score = models.IntegerField(
        choices    = StarChoices,
        editable   = False,
        validators = [
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')

    @cached_property
    def cached_average(self):
        cache_key = f"item_avg[{self.pk}]"
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value
            
        average_score = self.__class__.objects.filter(item=self.item).aggregate(avg_score=models.Avg('score'))['avg_score']
        cache.set(cache_key, average_score, 86400) # expire every 24 hour
        return average_score

    def clean(self):
        super().clean()
        if self.__class__.objects.filter(user=self.user, item=self.item).exists():
            raise ValidationError("You have already rated this item.")

    def __str__(self):
        return f"{self.score}"
    

class SellerItem(models.Model):
    item   = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_("Item"),   related_name='seller')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name=_("Seller"), related_name='item')
    count  = models.PositiveIntegerField()

    def __str__(self):
        return str(seller)
            

class Favorite(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='favorite')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')

    def __str__(self):
        return str(user)

