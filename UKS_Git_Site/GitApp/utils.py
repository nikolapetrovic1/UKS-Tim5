from django.shortcuts import get_object_or_404
from .models import *
from django.core.management import call_command


class MilestoneProgress:
    def __init__(self, open_issues, closed_issues, all_issues, percent):
        self.open_issues = open_issues
        self.closed_issues = closed_issues
        self.all_issues = all_issues
        self.percent = percent


def milestone_progress(milestone: Milestone):
    closed_issues = Issue.objects.filter(
        milestone=milestone, state=IssueState.CLOSED
    ).count()
    open_issues = Issue.objects.filter(
        milestone=milestone, state=IssueState.OPEN
    ).count()
    all_issues = Issue.objects.filter(milestone=milestone).count()
    percent = int((closed_issues / all_issues) * 100)
    return MilestoneProgress(open_issues, closed_issues, all_issues, percent)


def user_in_repository(repository_id, user_id):
    repository = get_object_or_404(Repository, id=repository_id)
    user = get_object_or_404(User, id=user_id)
    return user in repository.developers.all()


def reset_sequence():
    call_command("sqlsequencereset", "GitApp")
