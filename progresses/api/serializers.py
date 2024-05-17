from rest_framework import serializers

from progresses.models import Progress

class ProgressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Progress
        fields = (
            'id',
            'book',
            'user',
            'start_date',
            'finish_date',
            'is_completed',
        )