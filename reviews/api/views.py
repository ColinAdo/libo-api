from rest_framework import viewsets, permissions

from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

from reviews.models import Review

# Review viewset
class ReviewsViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)