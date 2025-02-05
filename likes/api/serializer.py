from rest_framework import serializers

from likes.models import Like

# Like book serializer
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Like
        fields = fields = ['id', 'user', 'book'] 