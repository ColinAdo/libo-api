from rest_framework import serializers

from reviews.models import Review
from likes.api.serializers import LikeReviewSeralizer

class ReviewSerializer(serializers.ModelSerializer):
    reviewed_by = serializers.ReadOnlyField(source='user.username')

    likes = LikeReviewSeralizer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()


    class Meta:
        model = Review
        fields = (
            'id',
            'reviewed_by',
            'book',
            'content',
            'likes',
            'likes_count',
            'date'
        )