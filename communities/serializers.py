from rest_framework import serializers
from .models import Community
from django.contrib.auth.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommunitySerializer(serializers.ModelSerializer):
    creator = UserShortSerializer(read_only=True)

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members_count', 'is_active', 'created_at', 'creator']

class CommunityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['name', 'description', 'members_count', 'is_active']