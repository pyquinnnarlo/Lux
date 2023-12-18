# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, File

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser  # Assuming you have a CustomUser model
        fields = ('username', 'password')