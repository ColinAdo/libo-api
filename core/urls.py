from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    # path('api/', include('djoser.urls.jwt')),
    path('api/', include('accounts.urls')),
    path('api/v1/', include('books.api.urls')),
    path('api/v1/', include('progresses.api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
