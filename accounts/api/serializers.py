from django.contrib.auth import get_user_model

from rest_framework import serializers

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'username',
        ]

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = get_user_model()
        fields = UserSerializer.Meta.fields + ["is_staff"]