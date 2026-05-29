from django.urls import path
from . import views, api_views
from notes.views import toggle_theme

app_name = 'notes'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('list/', views.note_list, name='note_list'),
    path('create/', views.create_note, name='create_note'),
    path('<int:note_id>/', views.note_detail, name='detail'),
    path('<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('<int:note_id>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('add-to-favorites/<int:note_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('clear-favorites/', views.clear_favorites, name='clear_favorites'),
    path('toggle-theme/', toggle_theme, name='toggle_theme'),
    path('api/notes/', api_views.NoteListAPIView.as_view(), name='api_notes'),
    path('api/notes/<int:pk>/', api_views.NoteDetailAPIView.as_view(), name='api_note_detail'),
    path('api/notes/create/', api_views.NoteCreateAPIView.as_view(), name='api_note_create'),
    path('api/notes/<int:pk>/update/', api_views.NoteUpdateAPIView.as_view(), name='api_note_update'),
    path('api/notes/<int:pk>/delete/', api_views.NoteDeleteAPIView.as_view(), name='api_note_delete'),
    path('api/comments/', api_views.CommentListAPIView.as_view(), name='api_comments'),
    path('api/comments/<int:pk>/', api_views.CommentDetailAPIView.as_view(), name='api_comment_detail'),
    path('api/notes/<int:note_id>/comments/', api_views.CommentCreateAPIView.as_view(), name='api_comment_create'),
    path('api/comments/<int:pk>/update/', api_views.CommentUpdateAPIView.as_view(), name='api_comment_update'),
    path('api/comments/<int:pk>/delete/', api_views.CommentDeleteAPIView.as_view(), name='api_comment_delete'),
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/<str:room_name>/', views.chat_room, name = 'chat_room')
]