from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=200)

class Star(models.Model):
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

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
