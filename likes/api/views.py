from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework.response import Response

from likes.api.serializers import LikeReviewSeralizer
from likes.models import LikeReview
from reviews.models import Review


# Like reviews view
class LikeReviewAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializers_class = LikeReviewSeralizer

    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            liked_reviews = LikeReview.objects.filter(review=review)

            serializer = LikeReviewSeralizer(liked_reviews, many=True)
            return Response({"success": True, "liked_review": serializer.data})
        
        except ObjectDoesNotExist:
            return Response({'success': 'False', 'message': 'review does not exist'})
        
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            new_liked_review = LikeReview.objects.get_or_create(user=request.user, review=review)

            if not new_liked_review[1]:
                new_liked_review[0].delete()
                return Response({"success": True, "message": "review unliked"})
            else:
                return Response({"success": True, "message": "review liked"})

        except ObjectDoesNotExist:
            return Response({'success': 'False', 'message': 'review does not exist'})
