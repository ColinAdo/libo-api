from rest_framework import generics

from books.models import Book
from books.api.serializers import BookSerializer

class BookListApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BoookDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer