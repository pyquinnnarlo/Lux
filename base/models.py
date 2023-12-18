from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # Add custom fields as needed
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    
class Repository(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    
class Branch(models.Model):
    name = models.CharField(max_length=100, default="master")
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    
    
class File(models.Model):
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files/', null=True)
    name = models.CharField(max_length=255) # Replace with the appropriate field for file content

    def __str__(self):
        return self.name

class Collaboration(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)