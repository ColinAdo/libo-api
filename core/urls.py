from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('accounts.api.urls')),
    path('api/v1/', include('books.api.urls')),
    path('api/v1/', include('progresses.api.urls')),
    path('api/v1/', include('favourites.api.urls')),
    path('api/v1/', include('reviews.api.urls')),
    path('api/v1/', include('likes.api.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
