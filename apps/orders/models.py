from django.db import models
from apps.core.models import LogicalBaseModel, StatusMixin, TimeStampBaseModel
from django.contrib.auth import get_user_model; User = get_user_model()
from apps.users.models import Address
from apps.items.models import Item

from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
from django.urls import reverse

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from django.core.cache import cache
from django.utils.functional import cached_property


class Order(TimeStampBaseModel, LogicalBaseModel, StatusMixin):
    class StatusChoices(models.TextChoices):
        IN_CARD        = "ICD", _("In Card")
        IN_ORDER       = "IOR", _("In Order")
        IS_PAID        = "IPD", _("Is Paid")
        IN_PROCESS     = "IPS", _("In Process")
        IN_PREPARATION = "IPN", _("In Preparation")
        SENDING        = "SDG", _("Sending")
        DELIVERED      = "DVD", _("Delivered")
        IS_DONE        = "IDE", _("Done")
    
    """\_______________[MAIN]_______________/"""
    status = models.CharField(
        max_length=3, 
        choices=StatusChoices,
        default="In Card",
        verbose_name = _("Order Item"),	
    )

    receiving_date = models.DateField()

    """\_____________[RELATIONS]_____________/"""
    item = models.ManyToManyField(
        to=Item,
        through      = "OrderItem",
        verbose_name = _("Order Item"),
        related_name = 'order',
    )

    user = models.ForeignKey(
        to=User,
        on_delete    = models.PROTECT,
        verbose_name = _("Customer"),
        related_name = 'order',
    )	


    address = models.ForeignKey(
        to=Address,
        on_delete    = models.PROTECT,
        verbose_name = _("Order Address"),
        related_name = 'order',
    )

    class Meta:
        verbose_name_plural = _("Orders")
        verbose_name        = _("Order")
        ordering            =  ("receiving_date",)

    def get_absolute_url(self):
        return reverse("orders:order_details", args=[self.id])

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    """\_______________[MAIN]_______________/"""
    count = models.PositiveIntegerField(verbose_name=_("Ordered Item Count"))

    """\_____________[RELATIONS]_____________/"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="order_item")


class DiscountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            expire_datetime__gte = timezone.now(),
            created_at__lte = timezone.now(),
            count__gt= 0,
        ) # only discounts that not expired & exists :)


class Discount(TimeStampBaseModel):
    class ModeChoices(models.TextChoices):
        PERCENT_MODE = "PM", _("Percent Mode")
        CASH_MODE    = "CM", _("Cash Mode")

    """\_______________[MAIN]_______________/"""
    mode = models.CharField(
        max_length=2,
        choices=ModeChoices, 
        default="Percent Mode"
    )

    percent = models.IntegerField(
        null=True,
        verbose_name=_("Percent"),
        validators = [
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )

    max_percent = models.IntegerField(
        null=True,
        default=100,
        verbose_name=_("Maximum Percent"),
        validators = [
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )

    cash = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=2,
        verbose_name=_("Cash"),
    )

    expire_datetime = models.DateTimeField(verbose_name=_("Expire Date & Time"))
    count = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_("Count"))

    """\_____________[RELATIONS]_____________/"""
    item  = models.OneToOneField(Item, null=True, on_delete=models.CASCADE, verbose_name=_('Item'))
    order = models.OneToOneField(Order, null=True, on_delete=models.CASCADE, verbose_name=_('Order'))

    objects = DiscountManager()

    class Meta:
        verbose_name_plural = _("Discounts")
        verbose_name        = _("Discount")

    def clean(self):
        super().clean()
        if timezone.now() < self.expire_datetime:
            raise ValidationError("The expiration datetime can't be before the current datetime! :(")

    def clean_mode(self):
        super().clean()
        if self.percent and self.cash:
            raise ValidationError("a Discount cant has both cash & percent mode! :(")

    def save(self, *args, **kwargs): # IS IT A BAD IDEA?!?!?!?!?!??!?!?!??!?!???!!?!?!?!??!?!?!?!?
        if self.expire_datetime:
            self.expire_datetime = datetime.strptime(self.expire_datetime, "%Y-%m-%d %H:%M:%S")
            self.expire_datetime = timezone.make_aware(self.expire_datetime)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.mode
