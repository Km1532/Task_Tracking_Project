from django import forms
from .models import Task
from .models import Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
