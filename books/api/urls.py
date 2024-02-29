from django.urls import path

from books.api.views import BookListApiView, BoookDetailsApiView

urlpatterns = [
    path('books/', BookListApiView.as_view(), name='books'),
    path('books/<int:pk>/', BoookDetailsApiView.as_view(), name='book_detail'),
]