from django.shortcuts import render
from .models import Achievement

# MOCK_ACHIEVEMENTS = [
#     {'name': 'Новичок', 'points': 10, 'description': 'Создал первую заметку', 'is_rare': False},
#     {'name': 'Автор месяца', 'points': 50, 'description': 'Опубликовал 10 заметок за месяц', 'is_rare': True},
#     {'name': 'Эксперт', 'points': 100, 'description': 'Получил 50 лайков на заметках', 'is_rare': True},
#     {'name': 'Помощник', 'points': 30, 'description': 'Прокомментировал 20 заметок', 'is_rare': False},
# ]

def achievement_list(request):
    achievements = Achievement.objects.all()
    context = {'achievements': achievements}
    return render(request, 'achievements/achievement_list.html', context)