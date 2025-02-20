from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from books.models import Book, Category
from books.api.serializers import BookSerializer, CategorySerializer

# Book viewset
class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-date_posted')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
