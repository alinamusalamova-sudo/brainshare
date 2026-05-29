from django.db import models
from django.contrib.auth.models import User
from communities.models import Community


class Note(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Текст заметки')
    subject = models.CharField('Предмет/дисциплина',max_length=100)
    is_important = models.BooleanField('Важное',default=False)
    created_at = models.DateTimeField('Дата создания',auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notes',verbose_name='Автор')
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True,  related_name='notes', verbose_name='Сообщество')
    image = models.ImageField('Картинка', upload_to='notes_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments', verbose_name='Заметка')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']  # сначала новые

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.note.title}'