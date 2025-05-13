from django.urls import path

from rest_framework.routers import DefaultRouter

from books.api.views import (
    BookViewset, 
    CategoryView, 
    LikedBooksView,
    AskChatPDFView,
    BookCategoryView,
    BookmarkedBooksView,
    AddPDFToChatPDFView
)

routes = DefaultRouter()

routes.register(r'books', BookViewset, basename='books')
urlpatterns = [
    path('liked/books/', LikedBooksView.as_view(), name='likes'),
    path('bookmarked/books/', BookmarkedBooksView.as_view(), name='bookmarks'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('books/category/<int:id>/', BookCategoryView.as_view(), name='book-category'),
    path('chatpdf/ask/', AskChatPDFView.as_view(), name='chatpdf-ask'),
    path('chatpdf/add/', AddPDFToChatPDFView.as_view(), name='chatpdf-add'),
]
urlpatterns += routes.urls