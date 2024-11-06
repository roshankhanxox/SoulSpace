from rest_framework import generics, views, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
from .models import UserProfile, Friend
from .serializers import UserProfileSerializer, FriendSerializer, MoodLogSerializer
from mood_logging.models import MoodLog  # Import MoodLog model for mood logs
from rest_framework.views import APIView


class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class MoodLogListView(generics.ListCreateAPIView):
    serializer_class = MoodLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodLog.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)

        # Define point values for each mood type
        mood_points = {
            "happy": 10,  # Positive mood
            "excited": 8,  # Positive mood
            "calm": 5,  # Neutral mood
            "anxious": -5,  # Negative mood
            "sad": -8,  # Negative mood
            "angry": -10,  # Negative mood
        }

        mood_type = serializer.validated_data["mood_type"]
        intensity = serializer.validated_data["intensity"]
        base_points = mood_points.get(
            mood_type, 0
        )  # Default to 0 if mood is not listed

        # Calculate final points based on mood and intensity
        final_points = base_points * intensity

        # Update the user's profile points with the calculated score
        user_profile.points += final_points
        user_profile.save()

        # Save the mood log entry
        serializer.save(user=self.request.user)


# class FriendListView(generics.ListCreateAPIView):
#     serializer_class = FriendSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Friend.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         user = self.request.user
#         friend_username = serializer.validated_data["friend_user"]

#         # Check if the user is trying to add themselves as a friend
#         if user.username == friend_username:
#             raise serializers.ValidationError("You cannot add yourself as a friend.")

#         # Look up the friend user by username
#         try:
#             friend_user = User.objects.get(username=friend_username)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Friend user does not exist.")

#         # Check if a friendship already exists in either direction
#         if (
#             Friend.objects.filter(user=user, friend_user=friend_user).exists()
#             or Friend.objects.filter(user=friend_user, friend_user=user).exists()
#         ):
#             raise serializers.ValidationError("Friendship already exists.")


#         # Create the friendship only if no existing friendship
#         serializer.save(user=user, friend_user=friend_user)
class FriendListView(generics.ListCreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Here, user will automatically be set by the serializer
        serializer.save(
            user=self.request.user
        )  # This will associate the logged-in user


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                # Add more fields if needed
            }
        )


class LeaderboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard = UserProfile.objects.order_by("-points")[:10]
        data = [
            {"username": profile.user.username, "points": profile.points}
            for profile in leaderboard
        ]
        return Response(data)
