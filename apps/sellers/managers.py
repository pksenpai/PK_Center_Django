from django.db import models


class SellerManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('user').filter(user__is_seller=True)
