from django.contrib.auth import get_user_model

from rest_framework import serializers

from progresses.api.serializers import ProgressSerializer
from books.models import Book, Category
from likes.api.serializer import LikeSerializer
from bookmark.api.serializers import BookmarkSerializer

class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = '__all__'

    def get_book_count(self, obj):
        return obj.books.count() 

# Book User serializer
class BookUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username')

# Book serializer
class BookSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    progress_count = serializers.SerializerMethodField()

    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    bookmarks = BookmarkSerializer(many=True, read_only=True)
    bookmarks_count = serializers.SerializerMethodField()

    readers = BookUserSerializer(many=True, read_only=True)
    readers_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            'id',
            'category',
            'author',
            'title',
            'cover_image',
            'pdf_file',
            'likes',
            'likes_count',
            'readers',
            'description',
            'readers_count',
            'progress',
            'progress_count',
            'bookmarks',
            'bookmarks_count',
            'readers_count',
            'date_posted'
        )
    
    def get_progress_count(self, obj):
        count = len(obj.progress.all())
        return count

    def get_likes_count(self, obj):
        count = len(obj.likes.all())
        return count

    def get_bookmarks_count(self, obj):
        count = len(obj.bookmarks.all())
        return count

    def get_readers_count(self, obj):
        count = len(obj.readers.all())
        return count