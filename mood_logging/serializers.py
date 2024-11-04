# moods/serializers.py

from rest_framework import serializers
from .models import MoodLog


class MoodLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoodLog
        fields = ["id", "user", "date", "mood_type", "intensity", "context"]
        read_only_fields = ["user", "date"]  # User and date are set automatically

    def create(self, validated_data):
        # Set the user field based on the logged-in user making the request
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
