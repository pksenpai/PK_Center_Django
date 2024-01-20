from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    # i18n_patterns(
    #     path('admin/', admin.site.urls),
    #     prefix_default_language=True,
    # ),
    path('admin/', admin.site.urls),
    path('account/', include('apps.users.urls')),
    path('items/', include('apps.items.urls')),
    path('orders/', include('apps.orders.urls')),
]
