from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from progresses.models import Progress
from progresses.api.serializers import ProgressSerializer
from favourites.models import Favourite
from favourites.api.serializers import FavouriteSerializer
from .serializers import UserSerializer

# Profile view
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, profId, *args, **kwargs):
        User = get_user_model()
        user = User.objects.get(profId=profId)

        if profId == request.user.profId:
            reading_books = Progress.objects.filter(user=user, is_reading=True)
            read_books = Progress.objects.filter(user=user, is_reading=False)
            book_saved = Favourite.objects.filter(user=user)

            reading_books_data = ProgressSerializer(reading_books, many=True).data
            read_books_data = ProgressSerializer(read_books, many=True).data
            book_saved_data = FavouriteSerializer(book_saved, many=True).data
            profile = UserSerializer(user).data

            if reading_books_data or read_books_data or book_saved_data:
                response_data = {
                    'profile': profile,
                    'reading_books': reading_books_data,
                    'read_books': read_books_data,
                    'book_saved': book_saved_data
                }
                return Response(response_data)
            else:
                return Response(profile)
        
        return Response({"Message": "You are not the owner..."})

