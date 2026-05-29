from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField('Название сообщества',max_length=200)
    description = models.TextField('Описание')
    members_count = models.IntegerField('Количество участников', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  related_name='created_communities', verbose_name='Создатель')

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.name