from django.db import models
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
        

class LogicalQuerySet(models.QuerySet):
    def delete(self):
        """
        - override delete method for querysets(multiple objs)
        - is_deleted objects is hide from users
        """
        return super().update(is_deleted=True)

    def hard_delete(self): # danger!!!
        """!!! delete all of that objs from database forever !!!"""
        return super().delete()


class LogicalManager(models.Manager):
    
    def get_queryset(self):
        """ only show objects that is unhide by default! """
        return LogicalQuerySet(self.model).filter(is_deleted=False, is_active=True)

    def archive(self):
        """ show all objects by this method | hide & unhide! no diff! """
        return LogicalQuerySet(self.model)

    def deleted(self):
        """ only show objects that is hide by this method! """
        return LogicalQuerySet(self.model).filter(is_deleted=True)


class LogicalBaseModel(models.Model):
    is_active = models.BooleanField(
        default      = True,
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
        return self.is_active and not self.is_deleted  # noqa


class ProfileImage(LogicalBaseModel, StatusMixin):
    """ low size images for User & Seller profiles """
    src = models.ImageField(upload_to='images/profile/')
    alt = models.CharField(max_length=255)
        
    class Meta:
        abstract = True

    def clean(self): # just for profiles image [o]
        super().clean()
        if self.src:
            width, height = self.src.width, self.src.height
            if width != height:
                raise ValidationError({_("image"): _("The image must be square :(")})


class ItemImage(LogicalBaseModel, StatusMixin):
    """ high size images for Item & Post media """
    src = models.ImageField(upload_to='images/item/')
    alt = models.CharField(max_length=255)
    
    class Meta:
        abstract = True
 
    
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
        to           = "apps.users.models.User",
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
        
    @property
    def author_full_name(self):
        "Returns the author's full name."
        return f"{self.author.first_name} {self.author.last_name}"
    
    def __str__(self):
        return str(self.author.get_full_name())


class OrderedByNewestComment(Comment):
    class Meta:
        ordering = ['created_at']
        proxy = True


class OrderedByOldestComment(Comment):
    class Meta:
        ordering = ['-created_at']
        proxy = True

    
class Report(TimeStampBaseModel):
    class ReaportChoices(models.TextChoices):
        INAPPROPRIATE_CONTENT = "IC", _("Inappropriate Content")
        INTELLECTUAL_PROPERTY = "IP", _("used my Intellectual Property without authorization")
        MATERIAL_PROPERTY     = "MP", _("used my Material Property without authorization")
        ANNOYING_CONTENT      = "AC", _("Annoying Content")
        POSTING_SPAM          = "PS", _("Posting Spam")
        PRETENDING            = "PS", _("Pretending to be Someone else")
    
    """\_______________[MAIN]_______________/"""
    reason      = models.CharField(choices=ReaportChoices, verbose_name=_("Reason"),)
    description = models.CharField(max_length=350, blank=True, null=True, verbose_name=_("Description"),)
    approved    = models.BooleanField(default=False, verbose_name=_("Approved"),)

    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey(
        to           = "apps.users.models.User",
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
        
    @property
    def reporter_full_name(self):
        "Returns the reporter's full name."
        return f"{self.reporter.first_name} {self.reporter.last_name}"
    
    def __str__(self):
        return f"{str(self.reporter.get_full_name())} reported {str(self.content_object)}"

