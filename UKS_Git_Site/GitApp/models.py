from django.db import models
from django.contrib.auth.models import AbstractUser


    
class Repository(models.Model):
    name = models.CharField(max_length=200)

class Star(models.Model):
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class User(AbstractUser):
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    stars = models.ManyToManyField(Star)
    repositories = models.ManyToManyField(Repository)
    role = models.CharField(max_length=200)
    

class Watcher(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
