import requests

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.conf import settings

from books.models import Book, Category
from books.api.serializers import BookSerializer, CategorySerializer

class AddPDFToChatPDFView(APIView):
    def post(self, request):
        pdf_url = request.data.get('url')
        if not pdf_url:
            return Response({'error': 'Missing PDF URL'}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'x-api-key': settings.CHATPDF_API_KEY,
            'Content-Type': 'application/json'
        }
        data = {'url': pdf_url}
        chatpdf_response = requests.post('https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

        if chatpdf_response.status_code == 200:
            source_id = chatpdf_response.json().get('sourceId')
            return Response({'sourceId': source_id}, status=200)
        else:
            return Response({
                'error': chatpdf_response.text
            }, status=chatpdf_response.status_code)
        
# class AskChatPDFView(APIView):
#     def post(self, request):
#         source_id = request.data.get('sourceId')
#         question = request.data.get('question')

#         if not source_id or not question:
#             print(f"Missing sourceId: {source_id}, question: {question}")
#             return Response({'error': 'Missing sourceId or question'}, status=400)

#         headers = {
#             'x-api-key': settings.CHATPDF_API_KEY,
#             'Content-Type': 'application/json'
#         }
#         data = {
#             'sourceId': source_id,
#             'messages': [
#                 {'role': 'user', 'content': question}
#             ]
#         }

#         chatpdf_response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

#         if chatpdf_response.status_code == 200:
#             answer = chatpdf_response.json()['content']
#             print(f"ChatPDF response: {answer}")
#             return Response({'response': answer}, status=200)
#         else:
#             return Response({'error': chatpdf_response.text}, status=chatpdf_response.status_code)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AskChatPDFView(APIView):
    def post(self, request):
        source_id = request.data.get('sourceId')
        question = request.data.get('question')

        if not source_id or not question:
            print(f"Missing sourceId: {source_id}, question: {question}")
            return Response({'error': 'Missing sourceId or question'}, status=400)

        headers = {
            'x-api-key': settings.CHATPDF_API_KEY,
            'Content-Type': 'application/json'
        }
        data = {
            'sourceId': source_id,
            'messages': [
                {'role': 'user', 'content': question}
            ]
        }

        chatpdf_response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

        if chatpdf_response.status_code == 200:
            answer = chatpdf_response.json()['content']
            print(f"ChatPDF response: {answer}")

            # Send to WebSocket
            channel_layer = get_channel_layer()
            user = request.user  # assumes the user is authenticated

            if user.is_authenticated:
                async_to_sync(channel_layer.group_send)(
                    user.username,
                    {
                        'type': 'chatpdf.message',
                        'message': answer,
                        'sourceId': source_id,
                    }
                )

            return Response({'response': answer}, status=200)
        else:
            return Response({'error': chatpdf_response.text}, status=chatpdf_response.status_code)


# Bookmarked Books by current logged in user view
class BookmarkedBooksView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        bookmarked_books = Book.objects.filter(bookmarks__user=user).distinct()
        serializer = BookSerializer(bookmarked_books, many=True)
        return Response(serializer.data)


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