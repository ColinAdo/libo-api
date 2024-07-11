from rest_framework import viewsets

from books.models import Book
from books.api.serializers import BookSerializer

# Book viewset
class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
