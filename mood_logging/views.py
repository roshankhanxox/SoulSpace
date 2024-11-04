# moods/views.py
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import MoodLog
from .serializers import MoodLogSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from .analysis import MoodTrendAnalysis


class MoodLogListCreateView(generics.ListCreateAPIView):
    serializer_class = MoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show mood logs for the logged-in user
        return MoodLog.objects.filter(user=self.request.user).order_by("-date")


class MoodLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MoodLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow detail view only for the mood logs of the logged-in user
        return MoodLog.objects.filter(user=self.request.user)


class MoodChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get mood logs for the last 30 days
        start_date = timezone.now() - timedelta(days=30)
        mood_logs = MoodLog.objects.filter(
            user=request.user, date__gte=start_date
        )  # Filter by user

        # Serialize mood logs
        serializer = MoodLogSerializer(mood_logs, many=True)
        return Response(serializer.data)


class MoodTrendView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user
        analysis = MoodTrendAnalysis(user)

        # Get mood trends for the last 30 days
        average_intensities = analysis.get_mood_trends(days=30)

        # Get content suggestions based on mood trends
        suggestions = analysis.suggest_content(average_intensities)

        return Response(
            {"average_intensities": average_intensities, "suggestions": suggestions}
        )
