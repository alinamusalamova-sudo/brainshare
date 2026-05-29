from rest_framework import generics
from .models import Achievement, UserAchievement
from .serializers import AchievementSerializer, UserAchievementSerializer

class AchievementListAPIView(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class AchievementDetailAPIView(generics.RetrieveAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class UserAchievementListAPIView(generics.ListAPIView):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer