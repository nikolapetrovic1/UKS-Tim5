from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=200)
    
class Repository(models.Model):
    name = models.CharField(max_length=200)
    #contributors = models.ForeignKey(User, on_delete=models.CASCADE)   // to remove comment when data is added to database

    def __str__(self):
        return self.name
