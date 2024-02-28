from django.urls import path

from books.api.views import BookListApiView

urlpatterns = [
    path('books/', BookListApiView.as_view(), name='books'),
]