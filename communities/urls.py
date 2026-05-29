from django.urls import path
from . import views, api_views

app_name = 'communities'

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('api/communities/', api_views.CommunityListAPIView.as_view(), name='api_communities'),
    path('api/communities/<int:pk>/', api_views.CommunityDetailAPIView.as_view(), name='api_community_detail'),
    path('api/communities/create/', api_views.CommunityCreateAPIView.as_view(), name='api_community_create'),
    path('api/communities/<int:pk>/update/', api_views.CommunityUpdateAPIView.as_view(), name='api_community_update'),
    path('api/communities/<int:pk>/delete/', api_views.CommunityDeleteAPIView.as_view(), name='api_community_delete'),
]