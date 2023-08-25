from django.db import models
from django.contrib.auth.models import AbstractUser
from polymorphic.models import PolymorphicModel


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
        return "{} - {}".format(self.name, self.color)


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
    forked_from = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        permissions = [
            ("can_delete_repository", "Can delete repository"),
        ]


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

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("name", "repository")


class DefaultBranch(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Default branch - {self.branch.name}"

    class Meta:
        unique_together = ("repository", "branch")


class Commit(models.Model):
    date_time = models.DateTimeField(auto_now=True)
    log_message = models.CharField(max_length=200)
    hash = models.CharField(max_length=200)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    commiter = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="commiter"
    )

    def __str__(self):
        date_time = self.date_time.strftime("%m/%d/%Y, %H:%M:%S")
        return (
            f"Commit {self.log_message} - {self.hash} by {self.commiter} at {date_time}"
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
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class PullRequest(Task):
    state = models.CharField(
        max_length=2, choices=State.STATE_CHOICES, default=State.OPEN
    )
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

    def __str__(self):
        return f"Pull requests '{self.state}' source - {self.source} target - {self.target}"


class Issue(Task):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_created = models.DateField(auto_now=True)
    labels = models.ManyToManyField(Label)
    state = models.CharField(
        max_length=2, choices=IssueState.STATE_CHOICES, default=IssueState.OPEN
    )

    class Meta:
        permissions = [
            ("can_create_issue", "Can create issue"),
        ]


class Event(PolymorphicModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    entity_type = models.CharField(max_length=200)
    entity_id = models.IntegerField()

    def __str__(self):
        return f"Event"


class IssueCreated(Event):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} created by {self.created_by} on {self.date_time.date()}"


class IssueUpdated(Event):
    title = models.CharField(max_length=200)
    changed_fields = models.TextField()

    def __str__(self):
        return f"{self.title} updated fields: {self.changed_fields} by {self.created_by} on {self.date_time.date()}"


class IssueClosed(Event):
    def __str__(self):
        return f"Issue closed by {self.created_by} on {self.date_time.date()}"


class IssueOpened(Event):
    def __str__(self):
        return f"Issue open by {self.created_by} on {self.date_time.date()}"


class Comment(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_by} - {self.content}"


class Reaction(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=20)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_by} - {self.code}"


# class StateChanged(Event):
#     new_state = models.ForeignKey(State, on_delete=models.CASCADE)
#
#
# class LabelApplication(Event):
#     label = models.ForeignKey(Label, on_delete=models.CASCADE)
