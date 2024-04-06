from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import DetailView, ListView
from .models import Task, Comment
from .forms import CommentForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('index')

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

class TaskListView(ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

def index_view(request):
    return render(request, 'index.html')

def account_view(request):
    if request.user.is_authenticated:
        return render(request, 'account.html')
    else:
        return redirect('login')

def contacts_view(request):
    return render(request, 'contacts.html')

def news_view(request):
    return render(request, 'news.html')

def feedback_view(request):
    return render(request, 'feedback.html')

def about_us_view(request):
    return render(request, 'about_us.html')

def soon_page(request):
    return render(request, 'soon_page.html')

def set_language(request):
    if request.method == 'POST' and request.is_ajax():
        language = request.POST.get('language')
        if language in ['uk', 'en']:
            request.session['selected_language'] = language
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def add_comment_to_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', pk=task_id)  
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_task.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')  
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

class RedirectUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path == reverse('account'):
            return redirect('login')
        return response
    

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})