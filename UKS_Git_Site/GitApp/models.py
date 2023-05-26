from django.db import models
from django.contrib.auth.models import AbstractUser


class State(models.Model):
    OPEN = "OP"
    CLOSED = "CL"
    MERGED = "MG"

    STATE_CHOICES = [
        (OPEN,"Open"),
        (CLOSED,"Closed"),
        (MERGED, "Merged"),
    ]

class Label(models.Model):
    name = models.CharField(max_length=200)

class User(AbstractUser):
    role = models.CharField(max_length=200)


class Project(models.Model):
    title = models.CharField(max_length=200)
    labels= models.ManyToManyField(Label)

class Repository(models.Model):
    name = models.CharField(max_length=200)
    contributors = models.CharField(
        max_length=200
    )  # to remove comment when data is added to database

    def __str__(self):
        return self.name



class Event(models.Model):
    date_time: models.DateTimeField()

class Task(models.Model):
    pass        

class Comment(Event):
    content: models.TextField(max_length=1500)
    date_created: models.DateTimeField(auto_now=True)
    task: models.ForeignKey(Task,on_delete=models.CASCADE)

class StateChanged(Event):
    new_state: State

class LabelApplication(Event):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

class Milestone(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateField()
    #Note: enums cannot be used with ForeignKey
    state = models.CharField(max_length=2,choices=State.STATE_CHOICES,default= State.OPEN) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

