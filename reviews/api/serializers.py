from rest_framework import serializers

from reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    reviewed_by = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Review
        fields = (
            'id',
            'reviewed_by',
            'book',
            'content',
            'date'
        )