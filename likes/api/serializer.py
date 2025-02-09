from rest_framework import serializers

from likes.models import Like

# Like book serializer
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'book'] 