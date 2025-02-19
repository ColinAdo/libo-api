from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('api/v1/books/', consumers.BookConsumer.as_asgi()),
]