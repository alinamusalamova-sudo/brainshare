from rest_framework import serializers
from .models import Note, Comment
from communities.models import Community
from django.contrib.auth.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommunityShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'author']


class NoteSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(read_only=True)
    community = CommunityShortSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'subject', 'is_important', 'created_at', 'author', 'community', 'comments',
                  'image']

class NoteCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'content', 'subject', 'is_important', 'community', 'image']

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']