from apps.users.models import Profile
from django.db import models
from .managers import SellerManager

from django.utils.translation import gettext_lazy as _


class Seller(Profile):
    rank = models.PositiveIntegerField(
        null=True,
        unique=True,
        verbose_name=_("Rank")
    )

    objects = SellerManager()

    class Meta:
        verbose_name_plural = _("Sellers")
        verbose_name        = _("Seller")
        ordering            =  ("rank",)

    def __str__(self):
        return self.name
