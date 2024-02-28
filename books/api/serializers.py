from django.contrib.auth import get_user_model

from  rest_framework import serializers

from books.models import Book, Review

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("id", "username")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    likes = UserSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    reviews = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()


    readers = UserSerializer(many=True, read_only=True)
    readers_count = serializers.SerializerMethodField()


    class Meta:
        model = Book
        fields = (
            "id",
            "category",
            "author",
            "title",
            "favourites",
            "cover_image",
            "pdf_file",
            "likes",
            "likes_count",
            "reviews",
            "reviews_count",
            "readers",
            "readers_count",
            "description",
            "date_posted"
        )

    def get_likes_count(self, obj):
        count = len(obj.likes.all())
        return count
    
    def get_reviews(self, obj):
        qs = obj.reviews.all()
        serializer = ReviewSerializer(qs, many=True).data
        return serializer
    
    def get_reviews_count(self, obj):
        count = len(obj.reviews.all())
        return count
    
    def get_readers_count(self, obj):
        count = len(obj.readers.all())
        return count

