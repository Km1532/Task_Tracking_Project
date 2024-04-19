"""
URL configuration for task_tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from trouble.views import CommentDeleteView, CommentUpdateView 
from trouble import views as trouble_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from trouble.models import Comment 
from trouble.views import (CommentDeleteView,CommentUpdateView, TaskCreateView,TaskListView,TaskDetailView,start_task,add_comment_to_task,delete_comment,edit_comment,my_password_reset,)


urlpatterns = [
    path('', trouble_views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/list/', TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('account/', trouble_views.account_view, name='account'),
    path('contacts/', trouble_views.contacts_view, name='contacts'),
    path('news/', trouble_views.news_view, name='news'),
    path('feedback/', trouble_views.feedback_view, name='feedback'),
    path('about/', trouble_views.about_us_view, name='about_us'),
    path('register/', trouble_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_password_reset/', my_password_reset, name='my_password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('soon_page/', trouble_views.soon_page, name='soon_page'),
    path('task/<int:pk>/start/', start_task, name='start_task'),
    path('task/<int:pk>/comment/', add_comment_to_task, name='add_comment_to_task'),
    path('task/<int:pk>/comment/<int:comment_pk>/delete/', login_required(CommentDeleteView.as_view()), name='comment_delete'),
    path('task/<int:pk>/comment/<int:comment_pk>/update/', login_required(CommentUpdateView.as_view()), name='comment_update'),
    path('task/<int:pk>/edit_comment/', edit_comment, name='edit_comment'),
    path('task/comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    path('like/comment/<int:pk>/', trouble_views.like_comment, name='like_comment'),
    path('set_language/', trouble_views.set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)