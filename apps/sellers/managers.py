from django.db import models


class SellerManager(models.Manager):
	"""
	If the user is not an staff or superuser, but the user is an admin seller,
	Then the profile is for the seller.
    """
	def get_queryset(self):
		return super().get_queryset().select_related('user').filter(
      		user__is_seller    = True,
      		user__is_staff     = False,
      		user__is_superuser = False,
        ) # So it is an admin seller :)
