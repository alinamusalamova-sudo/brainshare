from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from communities.models import Community
from achievements.models import Achievement
from django.contrib.auth.models import User
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import NoteForm
from django.http import HttpResponseRedirect



# MOCK_NOTES = [
#     {
#         'title': 'Основы Django',
#         'content': 'Django - это высокоуровневый фреймворк для веб-разработки на Python. Он позволяет быстро создавать сложные веб-приложения.',
#         'category': 'Программирование',
#         'is_important': True
#     },
#     {
#         'title': 'Как учить английский',
#         'content': 'Ежедневно читайте статьи, смотрите видео на английском и практикуйтесь с носителями языка.',
#         'category': 'Языки',
#         'is_important': False
#     },
#     {
#         'title': 'Топ-5 книг по Python',
#         'content': '1. Изучаем Python, 2. Автоматизация рутинных задач, 3. Python. К вершинам мастерства',
#         'category': 'Программирование',
#         'is_important': True
#     },
#     {
#         'title': 'Рецепт идеального кофе',
#         'content': 'Возьмите свежеобжаренные зерна, смолите, залейте водой 92°C во френч-прессе и настаивайте 4 минуты.',
#         'category': 'Лайфхаки',
#         'is_important': False
#     },
# ]

from django.contrib.auth.decorators import login_required

@login_required
def chat_room(request, room_name):
    return render(request, 'notes/chat.html', {'room_name': room_name})

def home_page(request):
    notes_count = Note.objects.count()
    communities_count = Community.objects.count()
    achievements_count = Achievement.objects.count()

    context = {
        'notes_count': notes_count,
        'communities_count': communities_count,
        'achievements_count': achievements_count,
    }
    return render(request, 'notes/home.html')

def note_list(request):
    notes = Note.objects.all()
    context = {'notes': notes}
    return render(request, 'notes/note_list.html', context)


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    comments = note.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.note = note
            new_comment.author = request.user
            new_comment.save()
            return redirect('notes:detail', note_id=note.id)
    else:
        form = CommentForm()

    context = {
        'note': note,
        'comments': comments,
        'form': form,
    }
    return render(request, 'notes/detail.html', context)


@login_required
def add_comment(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.author = request.user
            comment.save()

    return redirect('notes:detail', note_id=note.id)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return redirect('notes:detail', note_id=comment.note.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('notes:detail', note_id=comment.note.id)
    else:
        form = CommentForm(instance=comment)

    context = {
        'comment': comment,
        'form': form,
    }
    return render(request, 'notes/edit_comment.html', context)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    note_id = comment.note.id

    if comment.author != request.user:
        return redirect('notes:detail', note_id=note_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('notes:detail', note_id=note_id)

    context = {'comment': comment}
    return render(request, 'notes/delete_comment.html', context)


@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('notes:detail', note_id=note.id)
    else:
        form = NoteForm()

    return render(request, 'notes/create_note.html', {'form': form})


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        return redirect('notes:detail', note_id=note.id)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        return redirect('notes:detail', note_id=note.id)

    if request.method == 'POST':
        note.delete()
        return redirect('notes:list')

    return render(request, 'notes/delete_note.html', {'note': note})


def add_to_favorites(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    favorites = request.session.get('favorites', [])

    if note_id not in favorites:
        favorites.append(note_id)
        request.session['favorites'] = favorites

    return redirect('notes:detail', note_id=note.id)


def favorites_view(request):
    favorites_ids = request.session.get('favorites', [])
    notes = Note.objects.filter(id__in=favorites_ids)
    return render(request, 'notes/favorites.html', {'notes': notes})


def clear_favorites(request):
    request.session['favorites'] = []
    return redirect('notes:favorites')

def toggle_theme(request):
    current = request.COOKIES.get('theme', 'light')
    new = 'dark' if current == 'light' else 'light'
    resp = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    resp.set_cookie('theme', new, max_age=60*60*24*30)
    return resp