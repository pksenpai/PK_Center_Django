from django.urls import path
from .views import *


app_name = "orders"
urlpatterns = [
    path('cart/', CartView.as_view(), name="cart"),
    path('payment/', FinalizePaymentView.as_view(), name="payment"),
]
