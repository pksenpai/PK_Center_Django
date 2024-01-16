from django.db import models


class ProfileManager(models.Manager):
    """
    If the user is not a admin seller or staff or a superuser,
    then it is a customer who only uses the profile.
    """
    def get_queryset(self):
        return super().get_queryset().select_related('user').filter(
            user__is_seller=False,
            user__is_staff=False,
            user__is_superuser=False,
        ) # so it is a Customer! :)
