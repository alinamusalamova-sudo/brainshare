from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'author', 'is_important', 'created_at')
    list_filter = ('subject', 'is_important', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_important',)