from django.urls import path

from rest_framework.routers import DefaultRouter

from books.api.views import (
    BookViewset, 
    CategoryView, 
    LikedBooksView,
    BookCategoryView
)

routes = DefaultRouter()

routes.register(r'books', BookViewset, basename='books')
urlpatterns = [
    path('liked/books/', LikedBooksView.as_view(), name='likes'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('books/category/<int:id>/', BookCategoryView.as_view(), name='book-category'),
]
urlpatterns += routes.urls