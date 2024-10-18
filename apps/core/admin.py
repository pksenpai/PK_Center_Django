from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): ...

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin): ...

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin): ...
