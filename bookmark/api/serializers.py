from rest_framework import serializers

from bookmark.models import Bookmark

# Book mark serializer
class BookmarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'book'] 