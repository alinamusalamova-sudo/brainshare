from rest_framework import generics, permissions
from .models import Community
from .serializers import CommunitySerializer, CommunityCreateUpdateSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    summary="Список сообществ",
    description="Возвращает список всех сообществ",
    tags=['Сообщества']
)
class CommunityListAPIView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

@extend_schema(
    summary="Детальная информация о сообществе",
    description="Возвращает сообщество по его ID",
    tags=['Сообщества']
)
class CommunityDetailAPIView(generics.RetrieveAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

@extend_schema(
    summary="Создание сообщества",
    description="Создаёт новое сообщество",
    tags=['Сообщества'],
    request=CommunityCreateUpdateSerializer,
    responses={
        201: OpenApiResponse(description='Сообщество успешно создано'),
        400: OpenApiResponse(description='Ошибка валидации'),
        401: OpenApiResponse(description='Не авторизован'),
    }
)
class CommunityCreateAPIView(generics.CreateAPIView):
    serializer_class = CommunityCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

@extend_schema(
    summary="Обновление сообщества",
    description="Обновляет существующее сообщество",
    tags=['Сообщества'],
    request=CommunityCreateUpdateSerializer,
    responses={
        200: CommunitySerializer,
        400: OpenApiResponse(description='Ошибка валидации'),
        403: OpenApiResponse(description='Нельзя редактировать чужое сообщество'),
        404: OpenApiResponse(description='Сообщество не найдено'),
    }
)
class CommunityUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CommunityCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Community.objects.filter(creator=self.request.user)

@extend_schema(
    summary="Удаление сообщества",
    description="Удаляет сообщество",
    tags=['Сообщества'],
    responses={
        204: OpenApiResponse(description='Сообщество успешно удалено'),
        403: OpenApiResponse(description='Нельзя удалять чужое сообщество'),
        404: OpenApiResponse(description='Сообщество не найдено'),
    }
)
class CommunityDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Community.objects.filter(creator=self.request.user)