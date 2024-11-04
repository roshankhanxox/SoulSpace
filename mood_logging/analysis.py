from collections import defaultdict
from django.utils import timezone
from datetime import timedelta
from .models import MoodLog


class MoodTrendAnalysis:
    def __init__(self, user):
        self.user = user

    def get_mood_trends(self, days=30):
        # Get mood logs for the last 'days'
        start_date = timezone.now() - timedelta(days=days)
        mood_logs = MoodLog.objects.filter(user=self.user, date__gte=start_date)

        mood_intensity = defaultdict(list)

        # Aggregate mood intensity by mood type
        for log in mood_logs:
            mood_intensity[log.mood_type].append(log.intensity)

        # Calculate average mood intensity
        average_intensities = {
            mood: sum(intensities) / len(intensities)
            for mood, intensities in mood_intensity.items()
        }

        return average_intensities

    def suggest_content(self, average_intensities):
        suggestions = []

        for mood, intensity in average_intensities.items():
            if mood in ["sad", "anxious"] and intensity >= 3:
                suggestions.append(
                    {
                        "suggestion": f"Consider reading articles or watching videos about managing {mood}.",
                        "links": [
                            "https://www.verywellmind.com/how-to-deal-with-anxiety-2795843",  # Managing Anxiety
                            "https://www.psychologytoday.com/us/blog/the-meaning-psychopathology/201905/9-ways-improve-your-anxiety",  # Improving Anxiety
                            "https://www.healthline.com/health/anxiety-disorder/ways-to-manage-anxiety",  # Ways to Manage Anxiety
                            "https://www.nami.org/Your-Journey/Individuals-with-Mental-Illness/Anxiety-Disorders",  # NAMI Anxiety Disorders
                            "https://www.adaa.org/living-with-anxiety/podcasts",  # ADAA Podcasts
                        ],
                    }
                )

            if mood == "happy" and intensity >= 4:
                suggestions.append(
                    {
                        "suggestion": "Keep up the good vibes! Maybe try journaling your happy moments.",
                        "links": [
                            "https://www.psychologytoday.com/us/blog/the-happiness-project/201701/how-journaling-can-make-you-happier",  # Journaling Happiness
                            "https://greatergood.berkeley.edu/article/item/how_to_keep_a_happiness_journal",  # Happiness Journal
                            "https://www.thelittlejournal.com/how-journaling-boosts-your-happiness/",  # How Journaling Boosts Happiness
                            "https://www.journalprompt.com/journal-prompts-to-increase-happiness/",  # Journal Prompts for Happiness
                        ],
                    }
                )

            if mood == "calm" and intensity >= 4:
                suggestions.append(
                    {
                        "suggestion": "Explore meditation apps or calming music playlists.",
                        "links": [
                            "https://www.headspace.com/meditation-apps",  # Meditation Apps
                            "https://www.youtube.com/watch?v=1ZYbU82GVz4",  # Calming Music Playlist
                            "https://www.insider.com/best-meditation-apps",  # Best Meditation Apps
                            "https://www.psychologytoday.com/us/blog/minding-the-body/201908/how-to-calm-an-anxious-mind",  # Calm Anxious Mind
                            "https://www.healthline.com/health/meditation-for-beginners",  # Meditation for Beginners
                        ],
                    }
                )

        return suggestions


# from collections import defaultdict
# from django.utils import timezone
# from datetime import timedelta
# from .models import MoodLog


# class MoodTrendAnalysis:
#     def __init__(self, user):
#         self.user = user

#     def get_mood_trends(self, days=30):
#         # Get mood logs for the last 'days'
#         start_date = timezone.now() - timedelta(days=days)
#         mood_logs = MoodLog.objects.filter(user=self.user, date__gte=start_date)

#         mood_intensity = defaultdict(list)

#         # Aggregate mood intensity by mood type
#         for log in mood_logs:
#             mood_intensity[log.mood_type].append(log.intensity)

#         # Calculate average mood intensity
#         average_intensities = {
#             mood: sum(intensities) / len(intensities)
#             for mood, intensities in mood_intensity.items()
#         }

#         return average_intensities

#     def suggest_content(self, average_intensities):
#         suggestions = []

#         for mood, intensity in average_intensities.items():
#             if mood in ["sad", "anxious"] and intensity >= 3:
#                 suggestions.append(
#                     f"Consider reading articles or watching videos about managing {mood}."
#                 )

#             if mood == "happy" and intensity >= 4:
#                 suggestions.append(
#                     "Keep up the good vibes! Maybe try journaling your happy moments."
#                 )

#             if mood == "calm" and intensity >= 4:
#                 suggestions.append(
#                     "Explore meditation apps or calming music playlists."
#                 )

#         return suggestions
