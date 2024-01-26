from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # i18n_patterns(
    #     path('admin/', admin.site.urls),
    #     prefix_default_language=True,
    # ),
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')), # --> Home page
    path('account/', include('apps.users.urls')),
    path('items/', include('apps.items.urls')),
    path('orders/', include('apps.orders.urls')),
    path('sellers/', include('apps.sellers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
