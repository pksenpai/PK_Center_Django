from django.db import models


class Category(models.Model):
    """\_______________[MAIN]_______________/"""
    name = models.CharField(max_length=150)
    
    """\_____________[RELATIONS]_____________/"""
    sub = models.ForeignKey(
        to           = 'self',
        on_delete    = models.CASCADE,
        null         = True,
        blank        = True,
        related_name = "subs",
    )
    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    """\_______________[MAIN]_______________/"""
    body      = models.TextField()
    approved  = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey("apps.users.models.User", on_delete=models.CASCADE)
    
    reply  = models.ForeignKey(
        to           = 'self',
        on_delete    = models.CASCADE,
        null         = True,
        blank        = True,
        related_name = "replies",
    )
    
    """\___________[CONTENT_TYPE]___________/"""
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE) # item or post or seller or user table 
    object_id      = models.PositiveIntegerField() # item or post or seller or user id
    content_object = GenericForeignKey() # include both id & table
    
    def __str__(self):
        return str(self.author.get_full_name())
    
    
class Report(models.Model):
    class ReaportChoices(models.TextChoices):
        INAPPROPRIATE_CONTENT = "IC", _("Inappropriate Content")
        INTELLECTUAL_PROPERTY = "IP", _("used my Intellectual Property without authorization")
        MATERIAL_PROPERTY     = "MP", _("used my Material Property without authorization")
        ANNOYING_CONTENT      = "AC", _("Annoying Content")
        POSTING_SPAM          = "PS", _("Posting Spam")
        PRETENDING            = "PS", _("Pretending to be Someone else")
    
    """\_______________[MAIN]_______________/"""
    reason      = models.CharField(choices=ReaportChoices)
    description = models.CharField(max_length=350)
    approved    = models.BooleanField(default=False)
    date_time   = models.DateTimeField(auto_now_add=True)

    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey("apps.users.models.User", on_delete=models.CASCADE)
    
    """\___________[CONTENT_TYPE]___________/"""
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE) # post or user or seller
    object_id      = models.PositiveIntegerField() # reported id
    content_object = GenericForeignKey() # reported id from post or user or seller table
    
    def __str__(self):
        return f"{str(self.reporter.get_full_name())} reported {str(self.content_object)}"

