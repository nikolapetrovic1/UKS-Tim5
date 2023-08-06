from django.db import models

from .models import Issue, User


# class Event(models.Model):
#     created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     date_time = models.DateTimeField(auto_now=True)
#
#
# class IssueCreated(Event):
#     issue_id = models.ForeignKey(Issue, on_delete=models.DO_NOTHING)
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#
#
# class IssueClosed(Event):
#     issue_id = models.ForeignKey(Issue, on_delete=models.DO_NOTHING)
#
#
# class IssueOpened(Event):
#     issue_id = models.ForeignKey(Issue, on_delete=models.DO_NOTHING)


#
# class Issue(Task):
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     date_created = models.DateField(auto_now=True)
#     repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
#     labels = models.ManyToManyField(Label)
#     state = models.CharField(
#         max_length=2, choices=IssueState.STATE_CHOICES, default=IssueState.OPEN
#     )
