from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Note, Comment
from .serializers import NoteSerializer, CommentSerializer, NoteCreateUpdateSerializer, CommentCreateUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Список заметок",
    description="Возвращает список всех заметок",
    tags=['Заметки']
)
class NoteListAPIView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

@extend_schema(
    summary="Детальная информация о заметке",
    description="Возвращает заметку по её ID",
    tags=['Заметки']
)
class NoteDetailAPIView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

@extend_schema(
    summary="Создание заметки",
    description="Создаёт новую заметку",
    tags=['Заметки'],
    request=NoteCreateUpdateSerializer,
    responses={
        201: OpenApiResponse(description='Заметка успешно создана'),
        400: OpenApiResponse(description='Ошибка валидации'),
        401: OpenApiResponse(description='Не авторизован'),
    }
)
class NoteCreateAPIView(generics.CreateAPIView):
    serializer_class = NoteCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@extend_schema(
    summary="Обновление заметки",
    description="Обновляет существующую заметку",
    tags=['Заметки'],
    request=NoteCreateUpdateSerializer,
    responses={
        200: NoteSerializer,
        400: OpenApiResponse(description='Ошибка валидации'),
        403: OpenApiResponse(description='Нельзя редактировать чужую заметку'),
        404: OpenApiResponse(description='Заметка не найдена'),
    }
)
class NoteUpdateAPIView(generics.UpdateAPIView):
    serializer_class = NoteCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

@extend_schema(
    summary="Удаление заметки",
    description="Удаляет заметку",
    tags=['Заметки'],
    responses={
        204: OpenApiResponse(description='Заметка успешно удалена'),
        403: OpenApiResponse(description='Нельзя удалять чужую заметку'),
        404: OpenApiResponse(description='Заметка не найдена'),
    }
)
class NoteDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

@extend_schema(
    summary="Список комментариев",
    description="Возвращает список всех комментариев",
    tags=['Комментарии']
)
class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@extend_schema(
    summary="Детальная информация о комментарии",
    description="Возвращает комментарий по его ID",
    tags=['Комментарии']
)
class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@extend_schema(
    summary="Создание комментария",
    description="Добавляет новый комментарий к заметке",
    tags=['Комментарии'],
    request=CommentCreateUpdateSerializer,
    responses={
        201: OpenApiResponse(description='Комментарий успешно создан'),
        400: OpenApiResponse(description='Ошибка валидации'),
        401: OpenApiResponse(description='Не авторизован'),
    }
)
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.kwargs.get('note_id')
        note = get_object_or_404(Note, id=note_id)
        serializer.save(author=self.request.user, note=note)

@extend_schema(
    summary="Обновление комментария",
    description="Обновляет существующий комментарий",
    tags=['Комментарии'],
    request=CommentCreateUpdateSerializer,
    responses={
        200: CommentSerializer,
        400: OpenApiResponse(description='Ошибка валидации'),
        403: OpenApiResponse(description='Нельзя редактировать чужой комментарий'),
        404: OpenApiResponse(description='Комментарий не найден'),
    }
)
class CommentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

@extend_schema(
    summary="Удаление комментария",
    description="Удаляет комментарий",
    tags=['Комментарии'],
    responses={
        204: OpenApiResponse(description='Комментарий успешно удален'),
        403: OpenApiResponse(description='Нельзя удалять чужой комментарий'),
        404: OpenApiResponse(description='Комментарий не найден'),
    }
)
class CommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)