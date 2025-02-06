from django.urls import path

from rest_framework.routers import DefaultRouter

from books.api.views import BookViewset, CategoryView

routes = DefaultRouter()

routes.register(r'books', BookViewset, basename='books')
urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categories')
]
urlpatterns += routes.urls