from django.contrib import admin
from .models import Achievement, UserAchievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'points', 'is_rare', 'icon')
    list_filter = ('is_rare',)
    search_fields = ('name', 'description')
    list_editable = ('points', 'is_rare')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    list_filter = ('earned_at',)