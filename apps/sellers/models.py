from django.db import models
from apps.users.models import Profile
from apps.core.models import Category
from .managers import SellerManager

from django.utils.translation import gettext_lazy as _


class Seller(Profile):
    rank = models.PositiveIntegerField(
        null         = True,
        unique       = True,
        verbose_name = _("Rank")
    )

    category = models.ForeignKey(
        to           = Category,
        on_delete    = models.SET_NULL,
        null         = True,
        blank        = True,
        related_name = "sellers",
        verbose_name = _("Category"),
    )
    
    objects = SellerManager()

    class Meta:
        verbose_name_plural = _("Sellers")
        verbose_name        = _("Seller")
        ordering            =  ("rank",)

    def __str__(self):
        return self.name
