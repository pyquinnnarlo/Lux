from django.contrib import admin
from . models import CustomUser, Collaboration, Repository, File, Branch
# Register your models here.

admin.site.register([CustomUser, Collaboration, Repository, File, Branch])