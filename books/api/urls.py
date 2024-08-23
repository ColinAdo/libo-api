from django.urls import path

from rest_framework.routers import DefaultRouter

from books.api.views import BookViewset

routes = DefaultRouter()

routes.register(r'books', BookViewset, basename='books')
urlpatterns = routes.urls