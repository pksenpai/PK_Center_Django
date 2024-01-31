from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import ProfileImageBaseModel, LogicalBaseModel, StatusMixin
from django.contrib.auth.models import Group, Permission
from .managers import ProfileManager

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import RegexValidator


class User(AbstractUser, LogicalBaseModel):
    
    """\_______________[MAIN]_______________/"""
    is_active = models.BooleanField(
        _("active"),
        default=False,
    )
    
    # is_manager = models.BooleanField(
    #     _("manager"),
    #     default=False,
    # )
    
    is_supervisor = models.BooleanField(
        _("supervisor"),
        default=False,
    )
    
    is_operator = models.BooleanField(
        _("operator"),
        default=False,
    )
    
    email = models.EmailField(
        unique       = True,
        verbose_name = _("Email Address")
    )
    
    phone_number = models.CharField(
        max_length   = 50,
        null         = True,
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
    class Meta:
        verbose_name_plural = _("Users")
        verbose_name        = _("User")
        
    """\_______________[METHOD]_______________/"""
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        
        if self.is_staff and self.is_seller:
            group, created = Group.objects.get_or_create(name="Seller")
            if created:
                perms = Permission.objects.filter(
                    codename__in=[
                        'view_item',
                        'add_item',
                        'change_item',
                        'delete_item',

                        'view_discount',
                        'add_discount',
                        'change_discount',
                        'delete_discount',

                        'view_order',
                    ]
                )
                group.permissions.add(*perms)
            self.groups.add(group)
        
        # elif self.is_staff and self.is_superuser:...
        # elif self.is_staff and self.is_operator:...
        
            
    def __str__(self):
        return self.username


class Profile(ProfileImageBaseModel):

    """\_______________[MAIN]_______________/"""

    name = models.CharField(
        max_length   = 100,
        unique       = True,
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

    objects = ProfileManager()
    
    class Meta:
        verbose_name_plural = _("Profiles")
        verbose_name        = _("Profile")
        
    """\_______________[METHOD]_______________/"""

    def get_absolute_url(self):
        return reverse("users:profile", args=[self.id])

    def __str__(self):
        return str(self.name)
    

class Address(LogicalBaseModel, StatusMixin):
            
    """\_______________[MAIN]_______________/"""
    country = models.CharField(max_length=100, verbose_name=_('Country'))
    city    = models.CharField(max_length=100, verbose_name=_('City'))
    state   = models.CharField(max_length=100, verbose_name=_('State'))
    address = models.TextField(verbose_name=_('Address'))

    """\_______________[RELATION]_______________/"""

    user = models.ForeignKey(
            to           = User, 
            on_delete    = models.CASCADE,
            related_name = 'address',
            verbose_name = _('User'),
        )
    
    class Meta:
        verbose_name_plural = _("Addresses")
        verbose_name        = _("Address")
        ordering            =  ('city',)
        
    """\_______________[METHOD]_______________/"""

    def __str__(self):
        return str(self.user)
