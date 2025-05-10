from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from books.models import Book, Category
from books.api.serializers import BookSerializer, CategorySerializer

# Liked Books by current logged in user view
class LikedBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_books = Book.objects.filter(likes__user=user).distinct()
        serializer = BookSerializer(liked_books, many=True)
        return Response(serializer.data)


# Book viewset
class BookCategoryView(APIView):
    def get(self, request, id, format=None):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        books = Book.objects.filter(category=category)
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Book viewset
class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-date_posted')
    serializer_class = BookSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)    