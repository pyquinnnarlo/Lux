# github_app/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home,
    create_repository,
    repository_files,
    repository_detail,
    create_branch,
    user_repositories,
    upload_file,
    register,
    login_view,
    delete_file,
    delete_repository,
)

urlpatterns = [
    path('', home, name='home'),
    path('create_repository/', create_repository, name='create_repository'),
    path('repository_files/<int:repository_id>/', repository_files, name='repository_files'),
    path('repository_detail/<int:repository_id>/', repository_detail, name='repository_detail'),
    path('repository_detail/<int:repository_id>/<str:branch_name>/', repository_detail, name='repository_detail_with_branch'),
    path('upload_file/<int:repository_id>/<str:branch_name>/', upload_file, name='upload_file'),
    path('delete_file/<int:repository_id>/<int:file_id>/', delete_file, name='delete_file'),
    path('create_branch/<int:repository_id>/', create_branch, name='create_branch'),
    path('user_repositories/', user_repositories, name='user_repositories'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete_repository/<int:repository_id>/', delete_repository, name='delete_repository'),
    # Add other URL patterns as needed
]

