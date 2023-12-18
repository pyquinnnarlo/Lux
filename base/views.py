# github_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Repository, Collaboration, File, Branch
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm, CustomUserCreationForm, FileForm


def home(request):
    return render(request, 'home.html')

@login_required
def create_repository(request):
    if request.method == 'POST':
        name = request.POST['name']
        is_private = 'private' in request.POST
        repository = Repository.objects.create(name=name, owner=request.user, is_private=is_private)

        # Handle file upload
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            file_instance = File(repository=repository, file=uploaded_file)
            file_instance.save()

        return redirect('repository_detail', repository_id=repository.id)
    return render(request, 'create_repository.html')

def repository_files(request, repository_id):
    repository = get_object_or_404(Repository, pk=repository_id)
    files = File.objects.filter(repository=repository)
    return render(request, 'repository_files.html', {'repository': repository, 'files': files})

@login_required
def repository_detail(request, repository_id, branch_name=None):
    repository = get_object_or_404(Repository, id=repository_id)
    branches = Branch.objects.filter(repository=repository)

    # If a specific branch is selected, filter the branches
    selected_branch = None
    if branch_name:
        selected_branch = get_object_or_404(Branch, repository=repository, name=branch_name)

    # Handle file upload/update
    file_form = FileForm(request.POST, request.FILES)
    if request.method == 'POST' and file_form.is_valid():
        file_instance = file_form.save(commit=False)
        file_instance.repository = repository
        file_instance.branch = selected_branch  # Associate the file with the selected branch
        file_instance.save()

    # Handle branch deletion
    if request.method == 'POST' and 'delete_branch' in request.POST:
        branch_to_delete = get_object_or_404(Branch, repository=repository, name=request.POST['delete_branch'])
        branch_to_delete.delete()
        return redirect('repository_detail', repository_id=repository_id)

    context = {
        'repository': repository,
        'branches': branches,
        'selected_branch': selected_branch,
        'file_form': FileForm(),  # Pass an empty form for new file uploads
    }

    return render(request, 'repository_detail.html', context)

def upload_file(request, repository_id, branch_name):
    repository = get_object_or_404(Repository, id=repository_id)
    branch = get_object_or_404(Branch, repository=repository, name=branch_name)

    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        if file_form.is_valid():
            name = file_form.cleaned_data['name']
            file_instance = File(repository=repository, branch=branch, name=name, file=request.FILES['file'])
            file_instance.save()
            messages.success(request, 'File uploaded successfully.')
        else:
            messages.error(request, 'Error uploading file. Please check the form.')

    return redirect('repository_detail', repository_id=repository_id, branch_name=branch_name)
@login_required
def delete_file(request, repository_id, file_id):
    file_to_delete = get_object_or_404(File, repository__id=repository_id, id=file_id)
    file_to_delete.delete()
    return redirect('repository_detail', repository_id=repository_id)

@login_required
def create_branch(request, repository_id):
    if request.method == 'POST':
        repository = Repository.objects.get(id=repository_id)
        branch_name = request.POST['branch_name']

        # Check if branch with the same name already exists
        if not Branch.objects.filter(repository=repository, name=branch_name).exists():
            Branch.objects.create(name=branch_name, repository=repository)

    return redirect('repository_detail', repository_id=repository_id)

@login_required
def user_repositories(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            # If the user is a superuser, show all repositories
            repositories = Repository.objects.all()
        else:
            # For regular users, show public repositories and their own private repositories
            repositories = Repository.objects.filter(owner=user) | Repository.objects.filter(is_private=False)

        return render(request, 'user_repositories.html', {'repositories': repositories})
    else:
        # Handle the case where the user is not authenticated (optional)
        return render(request, 'user_repositories.html', {'repositories': []})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page URL pattern
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page URL pattern
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def delete_repository(request, repository_id):
    repository = get_object_or_404(Repository, id=repository_id)

    if request.method == 'POST':
        # If the form is submitted, delete the repository and redirect to a success page
        repository.delete()
        return redirect('user_repositories')  # Redirect to the repository list page or any other desired page

    # Render a confirmation page for deleting the repository
    return render(request, 'delete_repository.html', {'repository': repository})