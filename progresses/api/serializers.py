from rest_framework import serializers

from progresses.models import Progress

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = (
            'id',
            'book',
            'start_date',
            'finish_date',
            'is_completed',
        )