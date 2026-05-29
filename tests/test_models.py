import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from notes.models import Note, Comment
from communities.models import Community
from achievements.models import Achievement, UserAchievement
from users.models import Profile

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
class TestNote:
    def test_str(self, note):
        """Должен возвращать название заметки"""
        assert str(note) == "Введение в Django"

    def test_note_belongs_to_author(self, note, user):
        """Заметка должна принадлежать автору"""
        assert note.author == user

    def test_note_belongs_to_community(self, note, community):
        """Заметка должна принадлежать сообществу"""
        assert note.community == community


@pytest.mark.django_db
class TestComment:
    def test_comment_belongs_to_note_and_author(self, note, user):
        """Комментарий должен принадлежать заметке и автору"""
        comment = Comment.objects.create(
            note=note,
            author=user,
            text="Отличная заметка!",
        )
        assert comment.note == note
        assert comment.author == user


@pytest.mark.django_db
class TestCommunity:
    def test_str(self, community):
        """Должен возвращать название сообщества"""
        assert str(community) == "Python разработчики"

    def test_community_belongs_to_creator(self, community, user):
        """Сообщество должно принадлежать автору"""
        assert community.creator == user


@pytest.mark.django_db
class TestAchievement:
    def test_str(self, achievement):
        """Должен возвращать название достижения"""
        assert str(achievement) == "Первая заметка"

    def test_achievement_points_default(self):
        """Проверка значения по умолчанию для очков"""
        ach = Achievement.objects.create(
            name="Тестовое",
            description="Описание",
        )
        assert ach.points == 10


@pytest.mark.django_db
class TestProfileSignals:
    def test_profile_created_on_user_create(self):
        """При создании User должен автоматически создаваться Profile"""
        new_user = User.objects.create_user(username="ivan", password="pass")
        assert Profile.objects.filter(user=new_user).exists()


@pytest.mark.django_db
class TestUserAchievement:
    def test_user_achievement_connection(self, user, achievement):
        """Достижение должно привязываться к пользователю"""
        user_ach = UserAchievement.objects.create(
            user=user,
            achievement=achievement,
        )
        assert user_ach.user == user
        assert user_ach.achievement == achievement