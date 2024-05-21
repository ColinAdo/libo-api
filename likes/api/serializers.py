from rest_framework import serializers

from likes.models import LikeReview

class LikeReviewSeralizer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LikeReview
        fields = (
            'id', 
            'user',
            'review',
            'date'
        )