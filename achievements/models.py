from django.db import models
from django.contrib.auth.models import User


class Achievement(models.Model):
    name = models.CharField('Название достижения',max_length=200)
    description = models.TextField('Описание')
    points = models.IntegerField('Баллы',default=10)
    icon = models.CharField('Иконка',max_length=10, default='🏆')
    is_rare = models.BooleanField('Редкое',default=False)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements',  verbose_name='Пользователь')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, verbose_name='Достижение')
    earned_at = models.DateTimeField('Дата получения',auto_now_add=True)

    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"