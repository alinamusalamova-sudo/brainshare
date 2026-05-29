from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notes.models import Note, Comment
from communities.models import Community
from achievements.models import Achievement, UserAchievement
from users.models import Profile
from random import choice, randint


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = self._create_users()
        communities = self._create_communities(users)
        notes = self._create_notes(users, communities)
        self._create_comments(users, notes)
        achievements = self._create_achievements()
        self._assign_achievements(users, achievements)

        self.stdout.write(self.style.SUCCESS('База данных BrainShare успешно заполнена!'))

    def _create_users(self):
        User = get_user_model()
        users = []

        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser("admin", "admin@example.com", "admin123")
            Profile.objects.get_or_create(user=admin)
            self.stdout.write("Создали суперюзера admin")

        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={"email": f"user{i}@example.com"}
            )
            if created:
                user.set_password("password123")
                user.save()
                Profile.objects.get_or_create(user=user)
                self.stdout.write(f"Создали пользователя {user.username}")
            users.append(user)
        return users

    def _create_communities(self, users):
        names = ["Python разработчики", "Data Science", "Веб-дизайн", "Иностранные языки", "Книжный клуб"]
        communities = []

        for name in names:
            comm, _ = Community.objects.get_or_create(
                name=name,
                defaults={
                    "description": f"Сообщество для обсуждения {name.lower()}",
                    "members_count": randint(10, 500),
                    "is_active": choice([True, True, True, False]),
                    "creator": choice(users)
                }
            )
            communities.append(comm)
        self.stdout.write(f"Создали {len(communities)} сообществ")
        return communities

    def _create_notes(self, users, communities):
        subjects = ["Программирование", "Математика", "Английский", "Дизайн", "Психология"]
        titles = ["Введение в Django", "Как учить английский", "Топ книг по Python", "Рецепт идеального кофе",
                  "Основы Git", "Советы по верстке"]
        notes = []

        for i in range(20):
            note, _ = Note.objects.get_or_create(
                title=f"{choice(titles)} {i + 1}",
                defaults={
                    "content": "Это тестовое содержимое заметки. Здесь мог быть ваш полезный текст.",
                    "subject": choice(subjects),
                    "is_important": choice([True, False]),
                    "author": choice(users),
                    "community": choice(communities) if choice([True, False]) else None
                }
            )
            notes.append(note)
        self.stdout.write(f"Создали {len(notes)} заметок")
        return notes

    def _create_comments(self, users, notes):
        comments_count = 0
        for note in notes:
            for _ in range(randint(0, 5)):
                comment, created = Comment.objects.get_or_create(
                    note=note,
                    author=choice(users),
                    defaults={"text": "Отличная заметка! Спасибо!"}
                )
                if created:
                    comments_count += 1
        self.stdout.write(f"Создали {comments_count} комментариев")

    def _create_achievements(self):
        achievements_data = [
            {"name": "Первая заметка", "description": "Опубликовал первую заметку", "points": 10, "is_rare": False},
            {"name": "Активный автор", "description": "Опубликовал 10 заметок", "points": 50, "is_rare": False},
            {"name": "Популярный пост", "description": "Набрал 100 лайков", "points": 100, "is_rare": True},
            {"name": "Мастер комментариев", "description": "Оставил 50 комментариев", "points": 30, "is_rare": False},
            {"name": "Создатель сообщества", "description": "Создал новое сообщество", "points": 40, "is_rare": True},
        ]

        achievements = []
        for data in achievements_data:
            ach, _ = Achievement.objects.get_or_create(name=data["name"], defaults=data)
            achievements.append(ach)

        self.stdout.write(f"Создали {len(achievements)} достижений")
        return achievements

    def _assign_achievements(self, users, achievements):
        assigned = 0
        for user in users:
            for achievement in achievements[:randint(0, 3)]:
                _, created = UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement
                )
                if created:
                    assigned += 1
        self.stdout.write(f"Выдали {assigned} достижений пользователям")