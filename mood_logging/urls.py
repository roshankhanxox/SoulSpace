# moods/urls.py

from django.urls import path
from .views import (
    MoodLogListCreateView,
    MoodLogDetailView,
    MoodChartDataView,
    MoodTrendView,
)

urlpatterns = [
    path("logs/", MoodLogListCreateView.as_view(), name="moodlog-list-create"),
    path("logs/<int:pk>/", MoodLogDetailView.as_view(), name="moodlog-detail"),
    path("mood-chart-data/", MoodChartDataView.as_view(), name="mood_chart_data"),
    path("mood-trend/", MoodTrendView.as_view(), name="mood-trend"),
]
