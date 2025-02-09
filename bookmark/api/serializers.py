from rest_framework import serializers

from bookmark.models import Bookmark

# Book mark serializer
class BookmarkSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Bookmark
        fields = fields = ['id', 'user', 'book'] 