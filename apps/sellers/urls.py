from django.urls import path
from .views import *


app_name = "sellers"
urlpatterns = [
    path('profile/<int:pk>/', SellerProfileView.as_view(), name="profile"),
]
