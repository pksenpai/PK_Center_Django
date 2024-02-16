from django.urls import path
from .views import *

handler404 = 'apps.users.views.custom_404'
app_name = 'users'
urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path(
        'signup/',
        SignupView.as_view(),
        name='signup',
    ),
    path(
        'login/', 
        UsernameLoginView.as_view(),
        name='login',
    ),
    path(
        'email/', 
        EmailLoginView.as_view(),
        name='email',
    ),
    path(
        'email/otp/', 
        OTPView.as_view(),
        name='otp',
    ),
    path(
        'logout/',
        CustomLogoutView.as_view(), 
        name='logout',
    ),
    path('profile/<int:pid>/', Profile.as_view(), name='profile'),
    path('verify/<int:user_id>', VerifyUserView.as_view(), name='verify'),
]