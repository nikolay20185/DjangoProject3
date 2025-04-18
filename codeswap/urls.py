"""
URL configuration for codeswap project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('codeswap.apps.accounts.urls')),
    path('library/', include('codeswap.apps.library.urls')),
    path('community/', include('codeswap.apps.community.urls')),
    path('', include('codeswap.apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 