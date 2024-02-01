from django.db import models
from django.utils import timezone


class DiscountManager(models.Manager):
    def get_queryset(self):
        if self.model.percent_mode:
            return super().get_queryset().filter(
                expire_datetime__gte = timezone.now(),
                created_at__lte = timezone.now(),
            ) # only discounts that not expired :)
                    
        return super().get_queryset().filter(
            expire_datetime__gte = timezone.now(),
            created_at__lte = timezone.now(),
            count__gt= 0,
        ) # only discounts that not expired & exists :)
    
