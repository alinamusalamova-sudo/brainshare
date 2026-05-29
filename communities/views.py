from django.shortcuts import render
from .models import Community

# MOCK_COMMUNITIES = [
#     {'name': 'Python-разработчики', 'members': 50, 'description': 'Обсуждаем Python, Java, Django и др', 'is_active': True},
#     {'name': 'Изучаем английский', 'members': 90, 'description': 'Ежедневные занятия и разговорный клуб', 'is_active': True},
#     {'name': 'Data Science', 'members': 30, 'description': 'Машинное обучение и анализ данных', 'is_active': False},
# ]

def community_list(request):
    communities = Community.objects.all()
    context = {'communities': communities}
    return render(request, 'communities/community_list.html', context)