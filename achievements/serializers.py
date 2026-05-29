from rest_framework import serializers
from .models import Achievement, UserAchievement
from django.contrib.auth.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'points', 'is_rare']


class UserAchievementSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['id', 'user', 'achievement', 'earned_at']