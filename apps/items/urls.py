from django.urls import path
from .views import *


app_name = "items"
urlpatterns = [
    path('items-list/', ItemsList.as_view(), name="items_list"),
    path('item-details/<int:pid>/', ItemDetails.as_view(), name="item_details"),
]
