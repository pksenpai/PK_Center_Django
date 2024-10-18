from django.urls import path
from .views import *


app_name = "items"
urlpatterns = [
    path('list/', ItemsListView.as_view(), name="list"),
    path('details/<int:pk>/', ItemDetailsView.as_view(), name="details"),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name="category"),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name="seller"),
    # path('add/', AddToCartView.as_view(), name="add_cart"),
]
