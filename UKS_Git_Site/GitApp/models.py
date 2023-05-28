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
    labels = models.ManyToManyField(Label)
    lead = models.ForeignKey(User)
    developers = models.ManyToManyField(User,blank=True)

class Repository(models.Model):
    name = models.CharField(max_length=200)
    contributors = models.CharField(
        max_length=200
    )  # to remove comment when data is added to database
    
    #TODO: project relation
    def __str__(self):
        return self.name
class Branch(models.Model):
    repository = models.ForeignKey(Repository,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class Commit(models.Model):
    date_time: models.DateTimeField()
    log_message: models.CharField()
    hash: models.CharField()
    #TODO: parents
    author: models.ForeignKey(User)
    commiter: models.ForeignKey(User)

class Milestone(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    due_date = models.DateField()
    state = models.CharField(max_length=2,choices=State.STATE_CHOICES,default=State.OPEN) 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    creator = models.ForeignKey(User)
    assignees = models.ManyToManyField(User,blank=True)
    milestone = models.ForeignKey(Milestone)
class Event(models.Model):
    date_time: models.DateTimeField()
    task = models.ForeignKey(Task)

class Comment(Event):
    content: models.TextField(max_length=1500)
    date_created: models.DateTimeField(auto_now=True)
    task: models.ForeignKey(Task,on_delete=models.CASCADE)

class PullRequest(Task):
    target = models.ForeignKey(Branch,on_delete=models.CASCADE)
    source = models.ForeignKey(Branch,on_delete=models.CASCADE)
    
class Issue(Task):
    title: models.CharField(max_length=200)
    description: models.TextField()
    date_created: models.DateField()
    pull_request: models.ForeignKey(PullRequest)


class StateChanged(Event):
    new_state: State

class LabelApplication(Event):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)



