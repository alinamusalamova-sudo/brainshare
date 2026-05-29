from django.urls import path
from . import views, api_views

app_name = 'achievements'

urlpatterns = [
    path('', views.achievement_list, name='achievement_list'),
    path('api/achievements/', api_views.AchievementListAPIView.as_view(), name='api_achievements'),
    path('api/achievements/<int:pk>/', api_views.AchievementDetailAPIView.as_view(), name='api_achievement_detail'),
    path('api/user-achievements/', api_views.UserAchievementListAPIView.as_view(), name='api_user_achievements'),
]