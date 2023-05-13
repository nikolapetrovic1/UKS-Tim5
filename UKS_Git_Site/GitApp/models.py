from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Repository(models.Model):
    name = models.CharField(max_length=200)
    #contributors = models.ForeignKey(User, on_delete=models.CASCADE)   // to remove comment when data is added to database

    def __str__(self):
        return self.name
