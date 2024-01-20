from django.contrib import admin
from .models import *


@admin.register(Category)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(Comment)
class TaskAdmin(admin.ModelAdmin): ...

@admin.register(Report)
class TaskAdmin(admin.ModelAdmin): ...
