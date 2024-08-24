from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    ProgressViewset, 
    ReadView, 
    ChatPDFView,
    DeleteChatPDFView
)

route = DefaultRouter()
route.register(r'progress', ProgressViewset, basename='progress')

urlpatterns = [
    path('read/<int:pk>/', ReadView.as_view(), name='read'),
    path('chat/', ChatPDFView.as_view(), name='chat'),
]
urlpatterns += route.urls
