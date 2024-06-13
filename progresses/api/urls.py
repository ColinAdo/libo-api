from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProgressViewset, ReadView

route = DefaultRouter()
route.register(r'progress', ProgressViewset, basename='progress')

urlpatterns = [
    path('read/<int:pk>/', ReadView.as_view(), name='read'),
]
urlpatterns += route.urls
