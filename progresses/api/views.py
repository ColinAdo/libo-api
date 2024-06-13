from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import ProgressSerializer
from progresses.models import Progress
from progresses.signals import send_completion_email_after_seven_days
from books.models import Book

class ProgressViewset(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProgressSerializer

    def perform_create(self, serializer):
        progress = serializer.save(user=self.request.user)
        progress.set_finish_time()


class ReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        book = get_object_or_404(Book, pk=pk)

        if not book.readers.filter(id=user.id).exists():
            book.readers.add(user.id)
            created = Progress.objects.create(user=user, book=book, is_reading=True)
            created.set_finish_time()
            created.save()

            send_completion_email_after_seven_days.apply_async(args=[str(created.id)], countdown=1 * 60) 

        return Response(status=status.HTTP_200_OK)
