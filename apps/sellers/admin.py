from django.contrib import admin
from .models import *


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin): ...
