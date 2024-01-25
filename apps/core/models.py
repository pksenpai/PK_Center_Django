from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .managers import LogicalManager

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


"""\__________________[[Abstract Models]]__________________/"""

class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add = True,
        editable     = False,
        verbose_name = _("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now     = True,
        editable     = False,
        verbose_name = _("Update at"),
    )

    class Meta:
        abstract = True


class LogicalBaseModel(models.Model):
    is_active = models.BooleanField(
        default      = False,
        verbose_name = _("Active"),
    )
    
    is_deleted = models.BooleanField(
        default      = False,
        verbose_name = _("Deleted"),
    )

    objects = LogicalManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        - override delete method for one obj
        - is_deleted object is hide from users
        """
        self.is_deleted = True
        self.save()

    def hard_delete(self): # danger
        """ !!! delete that one obj from database forever !!! """
        super().delete()

    def undelete(self):
        """ unhide is_deleted object """
        self.is_deleted = False
        self.save()


class StatusMixin:
    @property
    def status(self) -> bool:
        return self.is_active and not self.is_deleted


class ProfileImageBaseModel(LogicalBaseModel, StatusMixin):
    """ low size images for User & Seller profiles """
    src = models.ImageField(upload_to='images/profile/', default='images/profile/default.png')
    alt = models.CharField(max_length=255)
        
    class Meta:
        abstract = True

    def clean(self): # just for profiles image [o]
        super().clean()
        if self.src:
            width, height = self.src.width, self.src.height
            if width != height:
                raise ValidationError({_("image"): _("The image must be square :(")})



 
    
"""\__________________[[Shared Models]]__________________/"""
class Category(models.Model):
    """\_______________[MAIN]_______________/"""
    name = models.CharField(max_length=150, unique=True, verbose_name=_("Name"),)
    
    """\_____________[RELATIONS]_____________/"""
    sub = models.ForeignKey(
        to           = 'self',
        on_delete    = models.CASCADE,
        null         = True,
        blank        = True,
        related_name = "subs",
        verbose_name = _("Sub Category"),
    )
    
    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name        = _("Category")
        ordering            =  ('name',)
        
    def __str__(self):
        return f"{self.name}"


class Comment(LogicalBaseModel, StatusMixin, TimeStampBaseModel):
    """\_______________[MAIN]_______________/"""
    body      = models.TextField(verbose_name=_("Body"),)
    approved  = models.BooleanField(default=False, verbose_name=_("Approved"),)
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(
        to           = "users.User",
        on_delete    = models.CASCADE,
        verbose_name = _("Author"),
    )
    
    reply  = models.ForeignKey(
        to           = 'self',
        on_delete    = models.CASCADE,
        null         = True,
        blank        = True,
        related_name = "replies",
        verbose_name=_("Reply"),
    )
    
    """\___________[CONTENT_TYPE]___________/"""
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE) # item or post or seller or user table 
    object_id      = models.PositiveIntegerField() # item or post or seller or user id
    content_object = GenericForeignKey() # include both id & table
    
    class Meta:
        verbose_name_plural = _("Comments")
        verbose_name        = _("Comment")
        
    def __str__(self):
        return str(self.author)


class OrderedByNewestComment(Comment):
    class Meta:
        ordering = ['created_at']
        proxy = True


class OrderedByOldestComment(Comment):
    class Meta:
        ordering = ['-created_at']
        proxy = True

    
REPORT_CHOICES = [
    ("IC", "Inappropriate content"),
    ("IP", "Used my intellectual property without authorization"),
    ("MP", "Used my material property without authorization"),
    ("AC", "Annoying content"),
    ("PS", "Posting spam"),
    ("PE", "Pretending to be someone else"),
]

class Report(TimeStampBaseModel):
    # class ReportChoices(models.TextChoices):
    #     INAPPROPRIATE_CONTENT = "IC", _("Inappropriate content")
    #     INTELLECTUAL_PROPERTY = "IP", _("Used my intellectual property without authorization")
    #     MATERIAL_PROPERTY     = "MP", _("Used my material property without authorization")
    #     ANNOYING_CONTENT      = "AC", _("Annoying content")
    #     POSTING_SPAM          = "PS", _("Posting spam")
    #     PRETENDING            = "PE", _("Pretending to be someone else")
    
    """\_______________[MAIN]_______________/"""
    reason      = models.CharField(max_length=3, choices=REPORT_CHOICES, verbose_name=_("Reason"),)
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name=_("Description"),)
    approved    = models.BooleanField(default=False, verbose_name=_("Approved"),)

    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey(
        to           = "users.User",
        on_delete    = models.CASCADE,
        verbose_name = _("Reporter"),
    )
    
    """\___________[CONTENT_TYPE]___________/"""
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE) # post or user or seller
    object_id      = models.PositiveIntegerField() # reported id
    content_object = GenericForeignKey() # reported id from post or user or seller table
    
    class Meta:
        verbose_name_plural = _("Reports")
        verbose_name        = _("Report")
        ordering            =  ('-created_at',)
        
    def __str__(self):
        return str(self.reporter)

