from rest_framework import serializers
from .models import UserProfile, Friend
from mood_logging.models import MoodLog  # Import the existing MoodLog model


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "points"]


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ["user", "friend_user", "added_at"]


class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ["mood_type", "intensity", "context", "date"]
