from django.db import models

# Create your models here.
# moods/models.py

from django.contrib.auth import get_user_model
from django.db import models
import datetime

User = get_user_model()


class MoodLog(models.Model):
    MOOD_CHOICES = [
        ("happy", "Happy"),
        ("sad", "Sad"),
        ("anxious", "Anxious"),
        ("calm", "Calm"),
        ("excited", "Excited"),
        ("angry", "Angry"),
        # Add more as necessary
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    mood_type = models.CharField(max_length=20, choices=MOOD_CHOICES)
    intensity = models.PositiveIntegerField(default=1)  # 1 to 5 scale for intensity
    context = models.TextField(blank=True, null=True)  # Optional user input

    def __str__(self):
        return f"{self.user.username} - {self.mood_type} on {self.date}"
