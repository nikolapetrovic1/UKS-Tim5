from django.db import models
from django.contrib.auth.models import AbstractUser


class IssueState(models.Model):
    OPEN = "OP"
    CLOSED = "CL"

    STATE_CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
    ]


class State(models.Model):
    OPEN = "OP"
    CLOSED = "CL"
    MERGED = "MG"

    STATE_CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
        (MERGED, "Merged"),
    ]


class RepositoryState(models.Model):
    PUBLIC = "PU"
    PRIVATE = "PR"

    STATE_CHOICES = [(PUBLIC, "Public"), (PRIVATE, "Private")]


class Label(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    color = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.name, self.description)


class User(AbstractUser):
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    role = models.CharField(max_length=200)


class Repository(models.Model):
    private = models.CharField(
        max_length=2,
        choices=RepositoryState.STATE_CHOICES,
        default=RepositoryState.PUBLIC,
    )
    name = models.CharField(max_length=200)
    labels = models.ManyToManyField(Label)
    lead = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="project_lead"
    )
    developers = models.ManyToManyField(
        User, blank=True, related_name="project_developer"
    )


class Star(models.Model):
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Watcher(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)


class Branch(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Commit(models.Model):
    date_time = models.DateTimeField(max_length=200)
    log_message = models.CharField(max_length=200)
    hash = models.CharField(max_length=200)
    # TODO: parents
    author = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="author"
    )
    commiter = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="commiter"
    )


class Milestone(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    due_date = models.DateField()
    state = models.CharField(
        max_length=2, choices=State.STATE_CHOICES, default=State.OPEN
    )
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.title, self.due_date)


class Task(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_creator"
    )
    milestone = models.ForeignKey(
        Milestone, blank=True, null=True, on_delete=models.SET_NULL
    )
    assignees = models.ManyToManyField(User, blank=True, related_name="task_assignee")


class Event(models.Model):
    date_time = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Comment(Event):
    content = models.TextField(max_length=1500)
    date_created = models.DateTimeField(auto_now=True)


class PullRequest(Task):
    target = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="target_branch",
    )
    source = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="source_branch",
    )


class Issue(Task):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateField(auto_now=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)
    state = models.CharField(
        max_length=2, choices=IssueState.STATE_CHOICES, default=IssueState.OPEN
    )


class StateChanged(Event):
    new_state = models.ForeignKey(State, on_delete=models.CASCADE)


class LabelApplication(Event):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
