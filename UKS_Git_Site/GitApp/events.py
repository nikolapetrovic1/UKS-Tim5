from django.db import models

from .models import *

# class Event(models.Model):
#       created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
#       date_time = models.DateTimeField(auto_now=True)

# class IssueCreated(Event):
#     id = models.ForeignKey(Issue,on_delete=models.DO_NOTHING)
#     title = models.TextField()
