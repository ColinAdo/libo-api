from rest_framework import serializers

from favourites.models import Favourite

class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Favourite
        fields = '__all__'