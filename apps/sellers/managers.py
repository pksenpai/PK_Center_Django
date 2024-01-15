from django.db import models


class SellerManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(is_seller=True)
