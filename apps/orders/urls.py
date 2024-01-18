from django.urls import path
from .views import *


app_name = "orders"
urlpatterns = [
    path('order-details/<int:oid>/', OrderDetails.as_view(), name="order_details"),
]
