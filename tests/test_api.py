import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from notes.models import Note
from communities.models import Community
from achievements.models import Achievement

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(username = "alina", password="pass123",email = "alina@gmail.com")

@pytest.fixture
def community(db, user):
    return Community.objects.create(
        name = "Python разработчики",
        description = "Обсуждаем питон и джанго",
        members_count=50,
        is_active=True,
        creator=user,
    )

@pytest.fixture
def note(db, user, community):
    return Note.objects.create(
        title="Введение в Django",
        content="Django - высокоуровневый фреймворк",
        subject="Программирование",
        is_important = True,
        author=user,
        community = community,
    )

@pytest.fixture
def achievement(db):
    return Achievement.objects.create(
        name = "Первая заметка",
        description = "опубликовал первую заметку",
        points = 10,
        is_rare=False

    )

@pytest.mark.django_db
def test_notes_api_returns_list(api_client, note):
    """Должен возвращать список заметок"""
    url = reverse('notes:api_notes')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['title'] == "Введение в Django"


@pytest.mark.django_db
def test_note_detail_returns_correct_data(api_client, note, community):
    """Должен возвращать детали заметки с вложенным сообществом"""
    url = reverse('notes:api_note_detail', kwargs={'pk': note.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Введение в Django"
    assert 'community' in data
    assert isinstance(data['community'], dict)
    assert data['community']['name'] == community.name


@pytest.mark.django_db
def test_communities_api_returns_list(api_client, community):
    """Должен возвращать список сообществ"""
    url = reverse('communities:api_communities')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['name'] == "Python разработчики"


@pytest.mark.django_db
def test_achievements_api_returns_list(api_client, achievement):
    """Должен возвращать список достижений"""
    url = reverse('achievements:api_achievements')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['name'] == "Первая заметка"
    assert data[0]['points'] == 10
