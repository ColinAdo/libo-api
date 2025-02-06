from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from books.models import Book, Category
from books.api.serializers import BookSerializer, CategorySerializer

# Book viewset
class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
