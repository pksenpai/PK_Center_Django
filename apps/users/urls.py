from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views # logout


app_name = 'users'
urlpatterns = [
    # path('signup/', signup, name='signup'),
    # path('login/', login_view, name='login'),
    path(
        'logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'
    ),
    path('profile/<int:pid>/', Profile.as_view(), name='profile'),
]