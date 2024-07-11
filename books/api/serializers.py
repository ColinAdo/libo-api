from django.contrib.auth import get_user_model

from rest_framework import serializers

from books.models import Book

from progresses.api.serializers import ProgressSerializer

# Book User serializer
class BookUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class BookSerializer(serializers.ModelSerializer):
    progress = ProgressSerializer(many=True, read_only=True)
    progress_count = serializers.SerializerMethodField()

    likes = BookUserSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    reviews = ProgressSerializer(many=True, read_only=True)
    reviews_count = serializers.SerializerMethodField()

    readers = BookUserSerializer(many=True, read_only=True)
    readers_count = serializers.SerializerMethodField()

    description = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "category",
            "author",
            "title",
            "cover_image",
            "pdf_file",
            "likes",
            "likes_count",
            "readers",
            "readers_count",
            "progress",
            "progress_count",
            "reviews",
            "reviews_count",
            "readers_count",
            "description",
            "text_content",
            "date_posted"
        )
        read_only_fields = ['text_content']
    
    def get_progress_count(self, obj):
        count = len(obj.progress.all())
        return count

    def get_likes_count(self, obj):
        count = len(obj.likes.all())
        return count

    def get_reviews_count(self, obj):
        count = len(obj.reviews.all())
        return count

    def get_readers_count(self, obj):
        count = len(obj.readers.all())
        return count

    def get_description(self, obj):
        if len(obj.description) < 80:
            return obj.description
        return f"{obj.description[:80]}..."
