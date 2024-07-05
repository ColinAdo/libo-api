from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import ProgressSerializer
from progresses.models import Progress
from progresses.signals import send_completion_email_after_seven_days
from books.models import Book

import requests

class ProgressViewset(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProgressSerializer

    def perform_create(self, serializer):
        progress = serializer.save(user=self.request.user)
        progress.set_finish_time()

# Read view 
class ReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        book = get_object_or_404(Book, pk=pk)

        headers = {
        'x-api-key': '',
        'Content-Type': 'application/json'
        }
        data = {'url': 'https://uscode.house.gov/static/constitution.pdf'}

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

        if response.status_code == 200:
            print('Source ID:', response.json()['sourceId'])
           
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)

        if not book.readers.filter(id=user.id).exists():
            book.readers.add(user.id)
            created = Progress.objects.create(user=user, book=book, is_reading=True)
            created.set_finish_time()
            created.save()

            send_completion_email_after_seven_days.apply_async(args=[str(created.id)], countdown=1 * 60) 

        return Response(status=status.HTTP_200_OK)
