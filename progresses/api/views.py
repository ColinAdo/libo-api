from rest_framework import viewsets, permissions

from .serializers import ProgressSerializer
from progresses.models import Progress

class ProgressViewset(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProgressSerializer

    def perform_create(self, serializer):
        progress = serializer.save(user=self.request.user)
        progress.set_finish_time()
