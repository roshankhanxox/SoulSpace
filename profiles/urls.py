from django.urls import path
from .views import (
    UserProfileView,
    MoodLogListView,
    FriendListView,
    LeaderboardView,
    UserDetailView,
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("moodlogs/", MoodLogListView.as_view(), name="mood-logs"),
    path("friends/", FriendListView.as_view(), name="friends-list"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("user/", UserDetailView.as_view(), name="user-detail"),
]
