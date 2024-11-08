# api/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("mood/", include("mood_logging.urls")),
    path("users/", UserListView.as_view(), name="user_list"),
    path("chatbot/", include("chatbot.urls")),
    path("profile/", include("profiles.urls")),
]
