from rest_framework import serializers
from .models import UserProfile, Friend
from mood_logging.models import MoodLog
from django.contrib.auth.models import User  # Import the existing MoodLog model


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["user", "points"]


class FriendSerializer(serializers.ModelSerializer):
    friend_user = serializers.CharField()  # Accepts a username as a string

    class Meta:
        model = Friend
        fields = ["user", "friend_user", "added_at"]

    def validate_friend_user(self, value):
        # Ensure the friend_user exists
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Friend user does not exist.")
        return value

    def create(self, validated_data):
        # Pop the username from the validated data
        friend_username = validated_data.pop("friend_user")
        user = validated_data["user"]

        # Retrieve the friend_user object using the username
        friend_user = User.objects.get(username=friend_username)

        # Create the Friend instance
        return Friend.objects.create(user=user, friend_user=friend_user)


class MoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLog
        fields = ["mood_type", "intensity", "context", "date"]
