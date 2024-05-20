from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import FavouriteSerializer
from favourites.models import Favourite
from books.models import Book

class FavouriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavouriteSerializer

    def get(self, request, *args, **kwargs):
        try:
            favourite = Favourite.objects.filter(user=request.user)
            serializer = FavouriteSerializer(favourite, many=True)

            return Response({"success": True, "favorite_books": serializer.data})
        except ObjectDoesNotExist:
            return Response({"success": True, "error": "favourite book does not exists" })
        
    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            new_favourite_book = Favourite.objects.get_or_create(user=request.user, book=book)

            if not new_favourite_book[1]:
                new_favourite_book[0].delete()
                return Response({"success": True, "message": "Book removed from favourites list"})
            else:
                return Response({"success": True, "message": "Book added to favourites list"})

        except ObjectDoesNotExist:
            return Response({"success": True, "error": "book does not exists"})

