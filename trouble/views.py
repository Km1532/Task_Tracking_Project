from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Task, Comment, Feedback
from .forms import CommentForm, TaskFilterForm, FeedbackForm
import logging
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import ProfileForm
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime

class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

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

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_update.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.task = self.object.task
        comment.user = self.request.user
        comment.save()
        return redirect('task_detail', pk=comment.task.pk)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comment_form = CommentForm(initial={'user': request.user})

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()

    user_avatar = request.user.profile.picture if hasattr(request.user, 'profile') else None

    return render(request, 'task_detail.html', {'task': task, 'comment_form': comment_form, 'user_avatar': user_avatar})

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'
    form_class = TaskFilterForm
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        if status and priority:
            queryset = queryset.filter(status__iexact=status.lower(), priority__iexact=priority.lower())
        elif status:
            queryset = queryset.filter(status__iexact=status.lower())
        elif priority:
            queryset = queryset.filter(priority__iexact=priority.lower())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form_class(self.request.GET)
        context['status'] = self.request.GET.get('status')
        context['priority'] = self.request.GET.get('priority')
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect('task_list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to']
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', pk=task.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return render(request, self.template_name, context)
        if task.status != 'Done' and task.due_date < datetime.now().date():
            task.status = 'Done'
            task.save()
        elif task.status == 'Done' and task.due_date >= datetime.now().date():
            task.status = 'Undone'
            task.save()

        return super().post(request, *args, **kwargs)


def index_view(request):
    return render(request, 'index.html')

@login_required
def account_view(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.username = request.POST.get('username')
            request.user.email = request.POST.get('email')
            request.user.save()
            return redirect('account')
    else:
        profile_form = ProfileForm(instance=request.user.profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email
        })
    
    return render(request, 'account.html', {'profile_form': profile_form})

    
    
def contacts_view(request):
    return render(request, 'contacts.html')

def news_view(request):
    return render(request, 'news.html')

logger = logging.getLogger(__name__)

@login_required
def feedback_view(request):
    if request.method == 'POST':
        logger.info('Received POST request for feedback')
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            logger.info('Form is valid')
            form.save()
            logger.info('Feedback saved successfully')
            return redirect('feedback')
        else:
            logger.error('Form is invalid: %s', form.errors)
    else:
        form = FeedbackForm(user=request.user)

    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'form': form, 'feedbacks': feedbacks})

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

@login_required
def add_comment_to_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task = task
            comment.save()
            return redirect('task_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'task_detail.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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

def start_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        if task.status != 'In Progress':
            task.status = 'In Progress'
            task.save()
        return redirect('task_detail', pk=pk)
    else:
        return HttpResponseForbidden()


def my_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
                subject = 'Reset your password'
                message = render_to_string('email/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url
                })
                send_mail(subject, message, 'from@example.com', [user.email])
                messages.success(request, 'Check your email for password reset instructions.')
                return redirect('login')
            else:
                messages.error(request, 'No user found with that email address.')
    else:
        form = PasswordResetForm()
    return render(request, 'my_password_reset.html', {'form': form})


@require_POST
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated:
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect('task_detail', pk=comment.task.pk)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        return redirect('task_detail', pk=comment.task.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=comment.task.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        task_pk = self.object.task.pk
        return reverse_lazy('task_detail', kwargs={'pk': task_pk})

    def get_object(self, queryset=None):
        comment_pk = self.kwargs.get('comment_pk')
        return get_object_or_404(Comment, pk=comment_pk)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    task_pk = comment.task.pk  
    if request.user == comment.user:
        comment.delete()
    return redirect(reverse('task_detail', kwargs={'pk': task_pk}))


