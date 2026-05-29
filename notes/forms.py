from django import forms
from .models import Note, Comment

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'subject', 'content', 'is_important', 'community', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название заметки'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Предмет/дисциплина'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Содержание заметки...'}),
            'is_important': forms.CheckboxInput(),
            'community': forms.Select(),
            'image': forms.ClearableFileInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']