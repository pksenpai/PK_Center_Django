from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import ProfileImageBaseModel, LogicalBaseModel, StatusMixin

from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    
    """\_______________[MAIN]_______________/"""
    
    email = models.EmailField(
        blank        = True,
        unique       = True,
        verbose_name = _("Email Address")
    )
    
    phone_number = models.CharField(
        max_length   = 50,
        blank        = True,
        unique       = True, 
        verbose_name = "Phone Number",
        validators   = [
            RegexValidator(
                regex=r'^(?:\+98|0)?9[0-9]{2}(?:[0-9](?:[ -]?[0-9]{3}){2}|[0-9]{8})$',
                message="Invalid phone number format. Example: +989123456789 or 09123456789",
            ),
        ], 
    )

    birth_date = models.DateField(
        null         = True,
        blank        = True,
        verbose_name = _('Birth Date')
    )

    """\_______________[ROLE]_______________/"""

    is_seller = models.BooleanField(
        default      = False,
        verbose_name = _('is seller?')
    )

    """\_______________[METHOD]_______________/"""

    def __str__(self):
        return self.username


class Profile(ProfileImageBaseModel):

    """\_______________[MAIN]_______________/"""

    name = models.CharField(
        max_length   = 100,
        verbose_name = _('Profile Name')
    )
    
    description = models.TextField(
        null         = True, 
        blank        = True,
        verbose_name = _('Description')
    )

    """\_______________[RELATION]_______________/"""

    user = models.OneToOneField(
            to           = User,
            on_delete    = models.CASCADE,
            verbose_name = _('User')
        )
    
    follows = models.ManyToManyField(
            to           = 'self',
            blank        = True,
            symmetrical  = False,
            related_name = "followed_by",
            verbose_name = _('Follows'),
        )

    """\_______________[METHOD]_______________/"""

    def get_absolute_url(self):
        return reverse("user_profile", args=[self.id])

    def __str__(self):
        return str(self.user)
    

class Address(LogicalBaseModel, StatusMixin):
            
    """\_______________[MAIN]_______________/"""
            
    city = models.CharField(max_length=100, verbose_name=_('City'))
    state = models.CharField(max_length=100, verbose_name=_('State'))
    address = models.TextField(verbose_name=_('Address'))

    """\_______________[RELATION]_______________/"""

    user = models.ForeignKey(
            to           = User, 
            on_delete    = models.CASCADE,
            related_name = 'address',
            verbose_name = _('User'),
        )
    
    """\_______________[METHOD]_______________/"""

    def __str__(self):
        return str(self.user)
