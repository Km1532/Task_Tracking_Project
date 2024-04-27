from django import forms
from .models import Task, Comment, Feedback, Profile
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].widget.attrs.update({'class': 'datepicker'})  

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():  
            raise forms.ValidationError("The end date must be in the future")
        return due_date

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = (
        ('', 'Any'),
        ('To Do', 'To Do'), 
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    )
    PRIORITY_CHOICES = (
        ('', 'Any'),
        ('Low', 'Low'),     
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text'] 
        widgets = {
            'user': forms.HiddenInput(),  
        }
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  
        if commit:
            instance.save()
        return instance

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']
