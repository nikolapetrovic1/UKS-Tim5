from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=200)
    
class Repository(models.Model):
    name = models.CharField(max_length=200)

class Star(models.Model):
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)

class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    stars = models.ManyToManyField(Star)
    repositories = models.ManyToManyField(Repository)

class Watcher(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)

    contributors = models.CharField(max_length=200)   # to remove comment when data is added to database

    def __str__(self):
        return self.name
