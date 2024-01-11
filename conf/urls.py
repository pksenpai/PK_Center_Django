from django.contrib import admin
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    i18n_patterns(
        path('admin/', admin.site.urls),
        prefix_default_language=True,
    )
]
